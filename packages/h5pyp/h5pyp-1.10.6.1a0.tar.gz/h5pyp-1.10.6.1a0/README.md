# h5pyp #
A Python package that contains the
[PARALLEL HDF5](https://portal.hdfgroup.org/display/HDF5/Parallel+HDF5)
*shared libraries* **and** the [h5py](https://pypi.org/project/h5py)
Python bindings.

The parallel version of the library will be compiled during the
installation process.

[h5pyp](https://pypi.org/project/h5pyp)
has been developed to be used in [LARGE](https://bitbucket.org/ncreati/large).

## Provides parallel (MPI enabled) h5py ##
[h5py](https://pypi.org/project/h5py) will be installed or reinstalled.

### Install the package ###
Install the latest stable version with

    pip3 install h5pyp

Or download the whole repository:

    git clone https://bitbucket.org/bvidmar/h5pyp

and then

    cd h5pyp

and install as preferred:

* python3 setup.py install
* pip3 install

### Test the installation ###
To test the installation run

    mpiexec -n 4 test_hdf5_parallel

This script will generate a *parallel_test.hdf5* in the current directory.
To show its content use the **h5pyp_dump** command:

    h5pyp_dump parallel_test.hdf5

the output should be:

     HDF5 "parallel_test.hdf5" {
     GROUP "/" {
        DATASET "test" {
           DATATYPE  H5T_STD_I32LE
           DATASPACE  SIMPLE { ( 4 ) / ( 4 ) }
           DATA {
           (0): 0, 1, 2, 3
           }
        }
     }
     }


----
**WARNING**

This is *alpha* code, use at your own risk.

----

### The Author ###
* [Roberto Vidmar](mailto://rvidmar@inogs.it)

### The mantainers ###
* [Roberto Vidmar](mailto://rvidmar@inogs.it)
* [Nicola Creati](mailto://ncreati@inogs.it)
