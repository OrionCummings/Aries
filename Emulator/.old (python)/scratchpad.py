import os
import inspect
debug  = lambda: str(os.path.split(inspect.stack()[1][1])[1]) + ":" + str(inspect.stack()[1][2]) + ":" + str(inspect.stack()[1][3]) + "()"

def a():
    print(debug())

def b():
    c()

def c():
    print(debug())


a()
b()
c()