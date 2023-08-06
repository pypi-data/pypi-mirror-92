**Package_VEnv-311:** 
**skestimate: https://pypi.org/project/skestimate/**
## How to publish the package:

A repository named EstimatorPkg is created on github and cloned locally. We put the meta data in the top level of this repo and create a package named skestimate as a subdirectory. This package is going to be published on test pypi. During development importing the package is done in the virtual environment to ensure consistency.

`(EstimatorPkg) EstimatorPkg%> python`
```
>>> import skestimate	# executes __init__.py inside skestimate. Import also creates a sub namespace for skestimate which can be viewed by dir(skestimate). We can have sub packages in the package by creating a subdirectory containing ann__init__.py file. 
```

### Here are the steps to follow:

1. Create the repo EstimatorPkg in the github with readme, git ignore for python and MIT license
2. Clone the repo onto the local machine. `repos%> git clone https://github.com/skhabiri/EstimatorPkg.git`
3. Use `pyenv install 3.7` to install a specific python version for the package
4. Create a virtual env for the project EstimatePkg. `EstimatorPkg %> pipenv --python 3.7`
   1. Now a virtual environment including a Pipfile has been created. Pipfile can be edited manually too. We install all the required packages inside an activated virtualenv to update the environment with all the requirements through Pipfile, and Pipfile.lock.
5. Activate the virtual env. `EstimatorPkg%> pipenv shell`
   1.  `(EstimatorPkg) EstimatorPkg%> which python`        # points to the location of a specified version of python used in virtual env
6. Install the required packages in the virtual env. `(EstimatorPkg) EstimatorPkg%> pipenv install numpy pandas scikit-learn matplotlib`
7. Create the package directory and __init__.py file. `(EstimatorPkg) skestimate%> touch __init__.py `
8. Code the python modules or subpackages as needed. (fit_est.py)
9. To test the package locally:
   1. `EstimatorPkg) EstimatorPkg%> python`        # launch CLI python repl
   2. `import skestimate`        # import the package
   3. `est = skestimate.example()`        #load cover_type dataset and create an instance of Xest
   4. est.xscore(fit=True)        # test any method of the class
10.  Add twine to the dev packages for uploading the package onto the pypi `(EstimatorPkg) skestimate%> pipenv install -d twine`
11. Create a setup.py and (build)[python setup.py sdist bdist_wheel] the actual package.
    1. The instruction for pypi is in setup.py as a meta file located at project directory (EstimatePkg). setup.py uses setuptools.setup() to define the package.
    2. Note that package names in pypi require an underscore to be changed to dashe as a pypi convention. 
12. `(EstimatorPkg) EstimatorPkg%> python setup.py sdist bdist_wheel`        # builds the package based on the setup file. The binary is specific to an OS. Now we should have dist and build directories and skestimate.egg-info, next to the package directory.
13. If not yet, register for a [test pypi account](https://test.pypi.org/account/register/)
14. Upload the package to the test pypi using `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
    1. #upload the content of the dist/ into test.pypi.org
    2. `twine upload dist/*` for pypi.org
15. Start a Colab notebook, and install the package, `!pip install --index-url https://test.pypi.org/simple/ your_package`
16. Import the package in the notebook, and try it out!

### Importing in main namespace and sub namespace

```
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

```
____

# Containers and Reproducible Builds-313:
Install Docker Desktop and create login in docker.com. Container can create a minimally required operating system that is more efficient in doing specialized work. Docker can also save on the hardware expenditure as it can create different environment on docker daemon and stream it to the docker client on our local machine. We can use our local machine and `docker` command to run a client docker or use a web based docker client as follows.
1. Log into https://labs.play-with-docker.com/
2. Add a new Instance
3. `apk add nano` adds nano text editor to the container. This is specific to the host OS distribution which is arch linux in this case, and it’s not related to the docker.
4. `which docker` verifies existence of docker.
5. `docker run hello-world`        # since it’s not recognised locally docker client contact docker daemon to pull the hello-world image from docker hub and create a docker container based on that image which runs an executable “hello from docker world” and stream it back to the docker client to print it on our local terminal.. 
6. `docker run -it debian /bin/bash`        # create a container based on debian distribution of linux with bash shell interactive mode.
7. `nano`                # doesn’t work anymore as we are in a new container. Now we are in debian linux not arch linux anymore.
8. `exit` we exit from debian and return to the jost arch linux OS that we were before
9. `docker run -it debian /bin/bash`        # will create a new container with a new hash numbers. The idea is containers are disposable and we can recreate them from images.
10. `apt update`                # update all the packages
11. `apt install python3`        # install python3 on the Debian distribution of Linux kernel.
12. `python3`                # we can run python3 on Debian Linux!
13. `apt-get install python3-pip`        # to get pip3
14. `pip3 install skestimate`        # we can test our package on Debian. Nice!
15. `docker image ls`        # shows all the local images available
16. `docker container ls -a`        # shows container ID and images available locally of the past containers that were recently run. Docker containers only save the differences vs original images and are usually small, but docker images by themselves could be large.
17.  `nano Dockerfile`        # allows us to create a tweaked image based on an existing docker hub image to be able to build a fresh container based on that image every time we launch docker run.
18.  `docker build . -t skestimate`                # build an image based on the Dockerfile in . and tag it with a specific name skestimate
19.  `docker image ls`        # in addition to debian and hello-world, lists skestimate as a local image available to build a container based on.
20.  `docker run -it skestimate`        #create a container based on an image which was originally built according to Dockerfile Dockerfile is a metafile located in the project (repository) directory not package directory. 
21. `docker image rm hello-world`        # We can remove unnecessary images to free up space. However, if there is a container dependent on that image, first we need to remove the container.
22. `docker container rm 91a3932b5cdc`, `docker image rm hello-world`, `docker image ls`
23. `docker run lambdata_skhab python3 -c "import skestimate; print(skestimate.example().xskew(0.9))"`        # without running the image interactively, it runs a command inside a freshly created container based on the image skestimate and exit.
24. Docker can be used for sharing software, and it can be published on hub.docker.com


###  Docker Container
Our goal is to test our sketimate package in a debian OS through docker image.
Here are the steps:
* Create the Dockerfile in EstimatePkg directory, which is the repository (project) directory. The specific instructions in Dockerfile are:
    * Based in”debian” image in dockerhub
    * bash shell
    * Python3 and pip3 installed
    * numpy, pandas, scikit-learn,  and matplotlib all installed
    * skestimate package installed
* Build the image on local machine with `docker build . -t skestimate_di`
* Very the existence of the new package with `docker image ls`
* Create and enter a fresh container with `docker run -it skestimate_di’
* Test the package with:
   * python3
   * import skestimate
   * est = skestimate.example()
   * est.xscore(fit=True)
   * exit()        #exit the python repl
* Exit the container with `exit`