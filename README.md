# UCFrame

UCFrame stands for a `Use Case Framework` designed to facilitate crowd-centric requirement acquisition. 

## Requirements

 * Python 2.7
 * TurboGears 2.3.4

Please check `install_requires` in `setup.py` for other packages. All needed packages are specified in `setup.py`, and will be automatically installed by following instructions.

## Installation and Launch

Install ``ucframe`` using the setup.py script::

    $ cd ucframe
    $ python setup.py develop

Create the project database for any model classes defined::

    $ gearbox setup-app

Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload --debug

Then you are ready to go.

## Associated Publication

 * W.-C. Hu, and H. C. Jiau, “UCFrame: A Use Case Framework for Crowd-Centric Requirement Acquisition,” ACM SIGSOFT Software Engineering Notes, vol. 41, no. 2, pp. 1-13, Mar. 2016. 