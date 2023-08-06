## 1. pip install nb_filelock

基于代码所在机器的跨进程 跨(jvm)解释器的文件互斥锁。兼容windwos和linux


filelock,which can run on linux and windwos.

```
比如希望在当前机器只能同时运行某一个代码块，完全豪不相关的两次启动xx.py，没有办法使用进程锁，
压根就不是使用multiprossing包同时启动的多个子进程而是手动两次运行了python xx.py，
好的方式是使用redis分布式锁，可以保证所有机器只提示一个获得锁，但如果没安装redis切要保证当前机器只有一个能执行代码块，
则使用此锁

```


### 测试例子。

```
把下面的python文件复制到一个文件中叫test.py,然后重复启动两次 python test.py，
当第一个脚本还没执行完代码块时候，另一个脚本会等待第一个脚本执行完成代码块的语句才会开始print hi。
```

```python
import nb_log
import time
from nb_filelock import FileLock

print('wait filelock')
with FileLock('testx.lock'):
    print('hi')
    time.sleep(20)
    print('hello')
```