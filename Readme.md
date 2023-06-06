## Configuration of spack

git clone -c feature.manyFiles=true https://github.com/spack/spack.git
source ./spack/share/spack/setup-env.sh

spack config add concretizer:reuse:false # will build from source instead of downloading the binaries.

We put configuration files in `spack/etc/spack` from the `config` directory.

```
ln -s config/compilers.yaml   ./spack/etc/spack/compilers.yaml
```

### Compilers

Gnu, amd and cray compilers were configured with compiler wrappers. ( not currently using the bare compilers )
Tested by installing zlib with all different compilers.
When using hdf5 spack links to all hdf5 implementations instead of just the one with the selected compiler. This is because spacks call a wrapper on the Cray wrapper and flags get mangled.  
Using the bare compilers avoids the problem. With mpich you should specify the prefix of the installation or it gets it wrong.


### Installing Cray libraries
- MPI
- BLAS 
- LAPACK
- HDF5
- FFTW
- NETCDF

Spack load does not modify the environment except for PATH , LD_LIBRARY_PATH variables etc. However Cray does not rely much on those variables, and seems to mostly rely on pkg-config. However PKG_CONFIG_PATH is not updated by spack load.
The module is fully loaded during the build environment.

## Using spack

`spack find`:  to view installed packages. Se `spack find -h` for options.
`spack install` 

### Creating packages

A template for a spack package can be created by typing
```
spack create --force --name hello_world https://github.com/lucaparisi91/hello_world/archive/refs/tags/v1.0.tar.gz
```


# Notes

You can use ftn --verbose to see the actual build commands which are invoked by the Cray wrapper.

# Tests

- install zlib with all compilers