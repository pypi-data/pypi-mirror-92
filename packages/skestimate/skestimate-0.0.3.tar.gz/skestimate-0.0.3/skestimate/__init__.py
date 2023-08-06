"""
fit a (pipelined) estimator and give a score report
"""


from .fit_est import Xest, example

"""
/src
    /pkg
        __init__.py
        foo.py
            foo_func()
            foo_func2()
        bar.py
    setup.py
    README.md
    LICENSE
If a package (directory) is imported, the python modules(file) 
underneath it by default are not available in the package namespace.
However, if a python module(file) is imported, all the functions of that will be 
available as the module attribute, and are available in the module namespace.
Importing packages or modules in python repl, adds names in the main namespace. 
Importing packages or modules in a package __init__.py, adds names to the package namespace.


----------------------
# __init__.py
# empty

>>> import pkg     
>>> dir()           # pkg is in the main namespace, NS
>>> dir(pkg)       # foo is not in the sub namespace, sNS
>>> pkg.foo         # foo not defined
----------------------
# __init__.py
# empty

>>> from pkg import foo     
>>> dir()                   # foo in the NS but pkg is not   
>>> pkg                     # error, pkg not defined
>>> pkg.foo                 # error, pkg not defined
>>> dir(foo)                # foo_func, and foo_func2 in sNS
>>> foo.foo_func            # available
----------------------
# __init__.py
from pkg import foo         # importing in pkg NS

>>> import pkg              # importing in main NS
>>> dir()                   # pkg in NS
>>> dir(pkg)                # foo in sNS
>>> dir(pkg.foo)            # both foo functions in sNS
----------------------
# __init__.py
from . import foo

>>> import pkg              
>>> dir()                   # pkg in NS
>>> dir(pkg)                # foo in sNS
>>> dir(pkg.foo)            # both foo functions in sNS
----------------------
# __init__.py
import pkg.foo

>>> import pkg              
>>> dir()                   # pkg in the NS
>>> dir(pkg)                # pkg and foo in sNS
>>> dir(pkg.foo)            # both foo functions in sNS
>>> foo                     # error
>>> pkg.pkg                 # points to pkg
----------------------
# __init__.py
from pkg.foo import foo_func

>>> import pkg              
>>> dir()                   # pkg in main NS
>>> dir(pkg)                # foo, foo_func in sNS
>>> pkg.foo                 # valid
>>> pkg.foo_func            # valid
>>> pkg.foo.foo_func        # same address as above
>>> pkg.foo_func2           # error, pkg has no attribute foo_func2
>>> pkg.foo.foo_func2       # valid
----------------------
# __init__.py
from .foo import foo_func

>>> import pkg              
>>> dir()                   # pkg in main NS
>>> dir(pkg)                # foo, foo_func in sNS
>>> pkg.foo                 # valid
>>> pkg.foo_func            # valid
>>> pkg.foo.foo_func        # same address as above
>>> pkg.foo_func2           # error, pkg has no attribute foo_func2
>>> pkg.foo.foo_func2       # valid
----------------------
# __init__.py
from foo import foo_func

>>> import pkg              # error, no module named foo
----------------------
"""

