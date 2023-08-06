# Jittor BY repo

这个仓库包含了计图的BY代码, 如果需要修改BY代码, 可以通过以下方式完成:

```bash
cd {jittor_path}/src
git clone https://github.com/jittor-online-first/__data__.git
```

把 `__data__` 仓库 clone 到 src 目录下以后, jittor就会自动编译这些代码, 而不是下载已经编译好的binary.

如果要把改好的 `__data__` 代码上线, 需要先编译好, 然后再 push 到该仓库, 编译并且上线的方法代码为 `python3.7 -m jittor.utils.polish`, 运行完成以后, 会生成最新的version string存放在
jittor主仓库里, 主仓库也需要同步 commit.