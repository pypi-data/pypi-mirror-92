import pkgutil
from live_recorder import you_live

print(you_live.__path__)

for filefiner, name, ispkg in pkgutil.iter_modules(you_live.__path__, ""):
    print("{0} name: {1:12}, is_sub_package: {2}".format(filefiner, name, ispkg))

if __name__ == '__main__':
     module = __import__('live_recorder.you_live')
     attrs = dir(module)
     print(attrs)