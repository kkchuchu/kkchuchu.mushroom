## 網路問題 -minutes

``` sh
nslookup
www.google.com.tw
```
NXDomain == Non-Existent domain


### 找檔案

``` sh
find . -name "*.png" -o -name "*.jpg" -o -name "*.gif" -type f
```

## Vim -minutes

### (ctrl-c ctrl-c)Send message from vim to other session

Enough of context, let's go to the solution

### Install [vim-slime](https://github.com/jpalardy/vim-slime);

### Go to the screen that will receive the text/command and run:
- screen -S SCREEN_NAME
- screen -ls | grep Attached | cut -f2
- it will return <pid>.SCREEN_NAME
- screen -X eval "msgwait 0"
- Go to the screen that will send the text/command and run:

### Go to the chunk of text you want to send or visually select it
- press C-c, C-c
- it will prompt screen session name:
- type <pid>.SCREEN_NAME from the other screen
- it will prompt screen window name: 0 press enter
- If it doesn't send right away the command, use C-c,C-c again.

### Reference
- https://coderwall.com/p/k-in2g/vim-slime-iterm2
- https://github.com/jpalardy/vim-slime

### NERDTREE Change Directory
- cd: change the CWD to the selected dir
- CD: change tree root to CWD
-
### Reference
- https://www.cheatography.com/stepk/cheat-sheets/vim-nerdtree/


## Python -minutes
### Multi-threads

![multi-treads](https://www.tutorialspoint.com/operating_system/images/thread_processes.jpg)

### User Level Threads vs Kernel Level Threads

User Level threads is managed by user and kernel Level threads is by os.

More detail can be found in the following link: https://www.tutorialspoint.com/operating_system/os_multi_threading.htm

### Python Global Intepreter Lock(GIL)

### Using Multiprocessing Library
Refer this [Link](http://zhuoqiang.me/python-thread-gil-and-ctypes.html)

### Does Python Access Module Variables Need Lock?

Yes! A lock is necessary. Look django dispatch.dispatcher.Signal.
This means module variable is shared by threads.

### property
``` python
class Egg(object):

    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price * RATE
    
    @price.setter
    def price(self, value):
        self._price = value
```

### iterator

has \_\_iter__ is iterable
and return an iterator

### coroutine

``` python
async def coro1():
    print("C1 start")
    print("C1 end")

c1 = coro1()
```

c1 is a coroutine object
await 表达式只有在本地协程(coroutine)函数里才是有效的

### \_\_init__ vs \_\_call__

``` python 
class foo:
    def __init__(self, a, b, c):
        pass

x = foo(1, 2, 3)

class foo:
    def __call__(self, a, b, c):
        pass

x = foo()
x(1, 2, 3)
```

### Use "if a is None"

### python module

mymodule.py
``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def rm(filename):
    os.remove(filename)
```

Python is somewhat of a sneaky snake when it comes to imports and managing modules. At runtime, the mymodule module has its own os which is imported into its own local scope in the module.


### mock.patch

mymodule.py
``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

def rm(filename):
    if os.path.isfile(filename):
        os.remove(filename)
```

Test Case for mymodule
``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mymodule import rm

import mock
import unittest

class RmTestCase(unittest.TestCase):
    
    @mock.patch('mymodule.os.path')
    @mock.patch('mymodule.os')
    def test_rm(self, mock_os, mock_path):
        # set up the mock
        mock_path.isfile.return_value = False
        
        rm("any path")
        
        # test that the remove call was NOT called.
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")
        
        # make the file 'exist'
        mock_path.isfile.return_value = True
        
        rm("any path")
        
        mock_os.remove.assert_called_with("any path")
```

Notice that decorator patch order and mock object property assign
