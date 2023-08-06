'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-26 10:54:43
LastEditors: xiaoshuyui
LastEditTime: 2021-01-26 14:19:10
'''
import sys
import inspect


def add(a, b):
    c = 3
    d = 4
    e = c + d
    return a + b + e


# class Tracer:

#     @classmethod
#     def dump(cls, frame, event, arg):
#         code = frame.f_code
#         module = inspect.getmodule(code)
#         module_name = ""
#         module_path = ""
#         if module:
#             module_path = module.__file__
#             module_name = module.__name__
#         print(event, module_path, module_name, code.co_name, frame.f_lineno,
#               frame.f_locals, arg)

#     def trace(self, frame, event, arg):
#         self.dump(frame, event, arg)
#         return self.trace

#     def collect(self, func, *args, **kwargs):
#         sys.settrace(self.trace)
#         func(*args, **kwargs)
#         sys.settrace(None)

class Tracer:
    plot = False
    section = 0

    @classmethod
    def dump(cls, frame, event, arg):
        code = frame.f_code
        module = inspect.getmodule(code)
        module_name = ""
        module_path = ""
        if module:
            module_path = module.__file__
            module_name = module.__name__
        if not cls.plot:
            print(event, module_name+'.'+str(code.co_name)+":"+
                  str(frame.f_lineno), frame.f_locals, arg)
            cls.section += 1
            print(cls.section)
        else:
            pass

    @classmethod
    def trace(cls, frame, event, arg):
        cls.dump(frame, event, arg)
        return cls.trace

    @classmethod
    def collect(cls, func, *args, **kwargs):
        sys.settrace(cls.trace)
        func(*args, **kwargs)
        sys.settrace(None)


if __name__ == "__main__":
    t = Tracer()
    t.collect(add, 1, 2)