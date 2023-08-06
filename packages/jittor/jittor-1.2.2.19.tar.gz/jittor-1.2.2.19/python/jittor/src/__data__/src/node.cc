// ***************************************************************
// Copyright (c) 2020 Jittor. Authors: Dun Liang <randonlang@gmail.com>. All Rights Reserved.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#include "pybind/py_var_tracer.h"
#include "mem/allocator.h"
#include "node.h"
#include "op.h"
#include "var.h"
#include "update_queue.h"

namespace jittor {

int64_t Node::tflag_count = 0;
int64_t nt = 0;

unordered_map<void*, int64> lived_nodes;
int64 total_node = 0;
vector<Node*> free_buffer;

static inline void free_var(Var* v) {
    if (v->mem_ptr != nullptr)
        v->allocator->free(v->mem_ptr, v->size, v->allocation);
    Var::number_of_lived_vars--;
    if (v->flags.get(NodeFlags::_in_update_queue))
        update_queue.pop(v);
}

void Node::free() {
    CHECK_EXIST;
    if (tflag == nt)
        return;
    // var can only be freed by backward_liveness
    // if var's input op is not freed, we need to keep it
    if (is_var() && (backward_liveness || _inputs.size())) {
        return;
    }
    tflag = nt;
    free_buffer.push_back(this);
    // release input
    for (auto i : _inputs) {
        i.node->_outputs.erase(i.back);
        if (!is_stop_grad()) {
            if (backward_liveness)
                i.node->release_backward_liveness();
            if (pending_liveness && !is_finished())
                i.node->release_pending_liveness();
        }
    }
    // release output
    for (auto o : _outputs) {
        o.node->_inputs.erase(o.back);
        if (!is_stop_grad()) {
            if (forward_liveness)
                o.node->release_forward_liveness();
        }
        if (o.node->is_var() && o.node->need_free())
            o.node->free();
    }
    if (is_var()) free_var((Var*)this);
}

void Node::__release() {
    if (is_var())
        Var::number_of_lived_vars--;
    else
        Op::number_of_lived_ops--;
    tflag = -1;
}

void Node::memcheck_all_exist() const {
#ifdef NODE_MEMCHECK
    CHECK_EXIST;
    for (auto& i : _inputs)
        CHECK_NODE_EXIST(i.node);
    for (auto& o : _outputs)
        CHECK_NODE_EXIST(o.node);
#endif
}

void Node::own_pending_liveness() {
    CHECK_EXIST;
    pending_liveness++;
    if (pending_liveness==1 && !is_finished())
        for (auto* i : inputs())
            i->own_pending_liveness();
}

void Node::release_pending_liveness() {
    CHECK_EXIST;
    pending_liveness--;
    if (!pending_liveness && !is_finished()) {
        // p2: output(p>0 and pending) contrib pending_liveness
        for (auto* i : inputs())
            i->release_pending_liveness();
    }
    if (need_free()) {
        LOGvvvv << "Free pending_liveness=0" << this;
        free();
    }
}

void Node::release_forward_liveness() {
    CHECK_EXIST;
    forward_liveness--;
    if (!forward_liveness) {
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (backward_liveness && !is_finished())
            release_pending_liveness();
        // f3. input(has_grad and f>0) contrib one forward_liveness
        if (!is_stop_grad()) {
            int n = outputs().size(), i=0;
            Node* os[n];
            for (auto* o : outputs()) {
                os[i++] = o;
            }
            for (int i=0; i<n; i++) {
                auto o = os[i];
                o->release_forward_liveness();
            }
        }
        if (pending_liveness) return;
        LOGvvvv << "Free forward_liveness=0" << this;
        free();
    }
}

void Node::own_forward_liveness() {
    CHECK_EXIST;
    forward_liveness++;
    if (forward_liveness==1) {
        // f2. input(has_grad and f>0) contrib one forward_liveness
        if (!is_stop_grad())
            for (auto* o : outputs())
                o->own_forward_liveness();
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (backward_liveness && !is_finished())
            own_pending_liveness();
    }
}

void Node::release_backward_liveness() {
    CHECK_EXIST;
    backward_liveness--;
    if (!backward_liveness) {
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (forward_liveness && !is_finished())
            release_pending_liveness();
        // b3. output(b>0) contrib one backward_liveness
        if (!is_stop_grad())
            for (auto* i : inputs())
                i->release_backward_liveness();
        if (pending_liveness) return;
        LOGvvvv << "Free backward_liveness=0" << this;
        free();
    }
}

void Node::own_backward_liveness() {
    CHECK_EXIST;
    backward_liveness++;
    if (backward_liveness==1) {
        // b3. output(b>0) contrib one backward_liveness
        if (!is_stop_grad())
            for (auto* i : inputs())
                i->own_backward_liveness();
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (forward_liveness && !is_finished())
            own_pending_liveness();
    }
}

void Node::own_both_liveness() {
    CHECK_EXIST;
    own_forward_liveness();
    own_backward_liveness();
}

void Node::release_both_liveness() {
    CHECK_EXIST;
    SetupFreeBuffer setup_free_buffer;
    release_forward_liveness();
    release_backward_liveness();
}

void Node::finish_pending_liveness() {
    CHECK_EXIST;
    if (is_finished()) return;
    SetupFreeBuffer setup_free_buffer;
    flags.set(NodeFlags::_finished);
    auto need_release = forward_liveness && backward_liveness;
    // p2: output(p>0 and pending) contrib pending_liveness
    if (pending_liveness)
        for (auto* i : inputs()) {
            i->release_pending_liveness();
        }
    if (need_release) {
        // p1: pending and f>0 and b>0 contrib pending_liveness
        release_pending_liveness();
    }
}

void Node::release_inputs() {
    CHECK_EXIST;
    if (!_inputs.size()) return;
    SetupFreeBuffer setup_free_buffer;
    for (auto i : _inputs) {
        if (!i.node->is_stop_grad() && i.node->forward_liveness)
            release_forward_liveness();
        i.node->_outputs.erase(i.back);
        if (!is_stop_grad() && backward_liveness)
            i.node->release_backward_liveness();
        if (pending_liveness)
            i.node->release_pending_liveness();
    }
    _inputs.clear();
}

void Node::set_inputs(list<Node*> nodes) {
    CHECK_EXIST;
    LOGvvvv << "Set inputs of" << this << "to" << nodes;
    ASSERT(!is_finished());
    // f2. input(has_grad and f>0) contrib one forward_liveness
    for (Node* node : nodes) {
        if (!node->is_stop_grad() && node->forward_liveness)
            own_forward_liveness();
        // we own liveness before release inputs
        // to prevent node be freed
        // b3. output(b>0) contrib one backward_liveness
        if (!is_stop_grad() && backward_liveness)
            node->own_backward_liveness();
        if (pending_liveness)
            node->own_pending_liveness();
    }
    release_inputs();
    bool is_var = this->is_var();
    auto inputs_iter = nodes.begin();
    for (size_t i=0; i<nodes.size(); i++, inputs_iter++) {
        Node* in = *inputs_iter;
        _inputs.emplace_back(in);
        in->_outputs.emplace_back(this, is_var?in->_outputs.size():i);
        _inputs.back().back = std::prev(in->_outputs.end());
        in->_outputs.back().back = std::prev(_inputs.end());
    }
}

// copy from set_inputs, remove release_inputs
void Node::add_inputs(const vector<Node*>& nodes) {
    CHECK_EXIST;
    LOGvvvv << "add inputs" << nodes << "to" << this;
    ASSERT(!is_finished());
    // f1. each input(need grad) contrib one forward_liveness
    for (Node* node : nodes) {
        if (!node->is_stop_grad() && node->forward_liveness)
            own_forward_liveness();
        // we own liveness before release inputs
        // to prevent node be freed
        // b3. output(b>0) contrib one backward_liveness
        if (!is_stop_grad() && backward_liveness)
            node->own_backward_liveness();;
        if (pending_liveness)
            node->own_pending_liveness();
    }
    bool is_var = this->is_var();
    auto inputs_iter = nodes.begin();
    uint psize = _inputs.size();
    for (size_t i=0; i<nodes.size(); i++, inputs_iter++) {
        Node* in = *inputs_iter;
        _inputs.emplace_back(in);
        in->_outputs.emplace_back(this, is_var?in->_outputs.size():i+psize);
        _inputs.back().back = std::prev(in->_outputs.end());
        in->_outputs.back().back = std::prev(_inputs.end());
    }
}

void Node::add_inputs(const vector<Var*>& nodes) {
    add_inputs((const vector<Node*>&)nodes);
}

void Node::set_stop_grad() {
    CHECK_EXIST;
    if (is_stop_grad()) return;
    SetupFreeBuffer setup_free_buffer;
    // can not set is_stop_grad from true to false
    flags.set(NodeFlags::_stop_grad, 1);
    // f3. input(has_grad and f>0) contrib one forward_liveness
    if (forward_liveness)
        for (Node* o : outputs())
            o->release_forward_liveness();
    // b3. output(b>0 and need grad) contrib one backward_liveness
    if (backward_liveness)
        for (Node* i : inputs())
            i->release_backward_liveness();
}

std::ostream& operator<<(std::ostream& os, const Node* node) {
    return node->is_var() ?  os << (const Var*)node : os << (const Op*)node;
}
} // jittor