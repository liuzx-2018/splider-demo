# coding=utf-8
'coding ING'
author = 'Rechard Liu'
class account(object):
    def set_name(self,name):
        self.__name=name
    def get_name(self):
        return self.__name

    def set_age(self,age):
        if 0 <age <=100:
            self.__age=age
        else:
            raise ValueError('bad score')

    def get_age(self):
        return self.__age

    def print_value(self):
        print(  self.__name ,':', self.__age)


barrt = account()
barrt.set_name('barrt')
barrt.set_age(19)
print(barrt.print_value())