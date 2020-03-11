from time import sleep
from wrapt_timeout_decorator import *


# timeout decorator needs to be in a different file on Windows OS
@timeout(5)
def mytest(message):
    print(message)
    for i in range(1,10):
        sleep(1)
        print('{} seconds have passed'.format(i))
