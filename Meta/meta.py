import inspect
"""Metaclass Definition """
 
class Parent(type):

    def __new__(meta, name, bases, dct):
        return super(Parent, meta).__new__(meta, name, bases, dct)

    def __init__(self,name, bases, dct):

        fmap={
                'get_':r"""def %(f)s(self) : return self._%(p)s""" , 
                'set_':r"""def %(f)s(self,%(p)s): self._%(p)s = %(p)s""" ,
                'del_':r"""def %(f)s(self): del self._%(p)s """ 
            }

        for p in inspect.getargspec(dct['__init__'])[0][1:]:
            t=[]
            for fname in ['get_' ,'set_','del_']:

                exec (fmap[fname] % { 'f' : fname + p , 'p' : p })
                exec ( 'func = %(f)s' % {'f' : fname + p })
                setattr(self,fname + p , func)
                t.append(func)

            setattr(self,name,property(t[0],t[1],t[2],""))
              

        super(Parent, self).__init__(name, bases, dct)

class Child(object):

    __metaclass__ = Parent

    def __init__(self,x=None,y=None,z=None):
        self._x = x
        self._y = y
        self._z = z

    
""" even though we didn't define the getter , setter and deleter 
    the metaclass will define them , python black magic :)"""
c=Child()

""" set x to a test string """
c.x = "Dummy test string """
try:
    assert c.x == "Dummy test string" 
except AssertionError as ae:
    print c.x


