// ***************************************************************
// Copyright (c) 2020 Jittor. Authors: 
//     Guowei Yang <471184555@qq.com>
//     Dun Liang <randonlang@gmail.com>. 
// All Rights Reserved.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#include <algorithm>
#include <functional>
#include "fuser.h"
#include "var.h"
#include "op.h"
#include "mem/allocator.h"
#include "graph.h"
#include "fused_op.h"

namespace jittor {

#define PREVENT_LARGE_FUSED_OP 16

void count_fuse(int64_t tt, int start_var_num, const vector<Op*>& ops, const vector<Var*>& vars, vector<int> &father, vector<int> &var_fused) {
    vector<int> dis(ops.size(), -1);
    
    auto find_fa = [&](int i) -> int {
        int j=i;
        while (father[j] != j) j = father[j];
        while (i != j) {
            int tmp = father[i];
            father[i] = j;
            i = tmp;
        }
        return j;
    };

    auto can_fuse = [&](Var* v, Op* op1, Op* op2, int fuse_type) -> bool {
        if (v->flags.get(NodeFlags::_stop_fuse))
            return false;
        if (fuse_type == 1) {
            // if v is output, do not fuse
            if (v->custom_data < start_var_num)
                return false;
            // op2 ---> v ---> op1
            if (op1->type() == OpType::other || op2->type() == OpType::other)
                return false;
            if (v->flags.get(NodeFlags::_force_fuse))
                return true;
            // Do not fuse op after reduce(has reduce)
            // TODO: better fuse strategy
            if (op2->type() == OpType::reduce)
                return false;
            // Do not fuse op before broadcast
            // TODO: better fuse strategy
            if (op1->type() == OpType::broadcast)
                return false;
            return op2->type() == OpType::element ||
                op2->type() == OpType::broadcast;
        } else if (fuse_type == 0) {
            #ifdef PREVENT_LARGE_FUSED_OP
            // This statement prevent fuse large ops 
            if (v->outputs().size()>=PREVENT_LARGE_FUSED_OP) return false;
            #endif

            // v ---> op1
            // |
            // +----> op2 ( prev of op1 )
            if (op1->type() == OpType::other || op2->type() == OpType::other)
                return false;
            // Do not fuse op after reduce(has reduce)
            // TODO: better fuse strategy
            if (op2->type() == OpType::broadcast || op1->type() == OpType::broadcast)
                return false;
            return true;
        }
        return false;
    };

    auto for_each_edge = [&](Op* op, int forward, auto&& func){
        auto e=op->_inputs.begin();
        for (Var* v : op->inputs()) {
            if ((forward && (*e).back!=std::prev(v->_outputs.end())) || 
            (!forward && (*e).back!=v->_outputs.begin())) {
                if ((*e).back->index>=0) {
                    auto next_edge = forward ? std::next((*e).back) : std::prev((*e).back);
                    if (next_edge->index>=0) {
                        Op* next_op = next_edge->node->op();
                        if (next_op && next_op->tflag==tt 
                            && next_op->custom_data != op->custom_data 
                            && can_fuse(v, next_op, op, 0))
                            func(v, next_op, 0);
                    }
                }
            }
            e = std::next(e);
        }

        if (forward) {
            for (Var* sv : op->outputs())
                if (sv && sv->tflag == tt)
                    for (auto next_op_e: sv->_outputs) {
                        // this is a control dependency edge, dont usedin op fuse
                        if (next_op_e.index<0) continue;
                        auto next_op = next_op_e.node->op();
                        if (next_op && next_op->tflag==tt) func(sv, next_op, 1);
                    }
        } else {
            for (auto sv_e : op->_inputs) {
                // this is a control dependency edge, dont usedin op fuse
                if (sv_e.back->index<0) continue;
                auto sv = sv_e.node->var();
                if (sv && sv->tflag == tt) func(sv, sv->input(), 1);
            }
        }
        
    };

    vector<int> queue;
    vector<int> deps;
    deps.reserve(ops.size());
    queue.reserve(ops.size());
    for (uint i=0; i<ops.size(); i++) {
        deps.push_back(0);
        Op* op = ops[i];

        for_each_edge(op, 1, [&](Var* v, Op* next_op, int real_edge) {
            deps[i]++;
        });
        
        if (!deps[i]) {
            queue.push_back(i);
            dis[i]=0;
        }
    }

    uint head=0;
    while (head<queue.size()) {
        int op_id=queue[head++];
        Op* op = ops[op_id];

        for_each_edge(op, 1, [&](Var* v, Op* next_op, int real_edge) {
            int next_id = next_op->custom_data;
            if (dis[next_id] == dis[op_id]){
                int next_fa = find_fa(next_id);
                father[next_fa] = op_id;
            }
        });

        for_each_edge(op, 0, [&](Var* v, Op* next_op, int real_edge) {
            int next_id = next_op->custom_data;
            int lon=0;
            if (real_edge && !can_fuse(v, op, next_op, 1)) lon=1;
            if (dis[op_id]+lon>dis[next_id])
                dis[next_id]=dis[op_id]+lon;
            if (!--deps[next_id]) queue.push_back(next_id);
        });
    }

    if (V_ON(1000)) {
        for (uint i=0; i<ops.size(); i++)
            LOGvvvv << ops[i] << dis[i] << deps[i];
    }
    for (uint i=0; i<vars.size(); i++) {
        Var* v = vars[i];
        if (!v || v->tflag!=tt) {
            var_fused[i]=1;
            continue;
        }
        // sf: input op's father id
        int sf = -1;
        // vf: is input op can be fused with all output op
        int vf = 1;
        // all outputs are reduce
        int all_reduce = 1;
        Op* iop = v->input();
        // if (iop && iop->tflag==tt) 
        sf = find_fa(iop->custom_data);

        for (Op* sop : v->outputs())
            if (sop->tflag==tt) {
                if (vf && !can_fuse(v,sop,iop,1))
                    vf = 0;
                if (sop->type()!=OpType::reduce)
                    all_reduce = 0;
                // in two different fused op
                if (find_fa(sop->custom_data)!=sf) {
                    var_fused[i]=1;
                }
            }
        if (vf==0)
            // cannot fused
            var_fused[i]=1;
        else if (var_fused[i]) {
            if (iop->type()==OpType::broadcast || 
                all_reduce || 
                v->flags.get(NodeFlags::_force_fuse))
                // strong fused
                var_fused[i] = 3;
            else {
                // check weak fused
                // var_fused[i] = 2;
                if (v->dtype() == ns_bool || iop->inputs().size()>2)
                    var_fused[i] = 1;
                else if (iop->inputs().size() == 2) {
                    auto a = iop->inputs().front()->input();
                    auto b = iop->inputs().back()->input();
                    // TODO: better detect weak binary op(such as max(a, 0)
                    if ((a && a->type()==OpType::broadcast) || 
                        (b && b->type()==OpType::broadcast))
                        var_fused[i] = 2;
                    else
                        var_fused[i] = 1;
                } else
                   var_fused[i] = 2;
            }
        }
    }
    // output vars can not be fused
    for (int i=0; i<start_var_num; i++)
        var_fused[i] = 1;
}
    
} // jittor