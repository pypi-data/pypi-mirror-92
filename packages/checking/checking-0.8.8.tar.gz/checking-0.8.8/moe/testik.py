from checking import *


@test
def api_check():
    common['1']=1
    equals(4, 2 + common.value) # Here we use common - object available from all tests
    print(common)


if __name__ == '__main__':
    start(verbose=3, params={'value': 2}) # Here we adds a parameter to common object
