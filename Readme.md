## Configuration of spack

git clone -c feature.manyFiles=true https://github.com/spack/spack.git
source ./spack/share/spack/setup-env.sh

spack config add concretizer:reuse:false # will build from source instead of downloading the binaries.

We put configuration files in `spack/etc/spack` from the `config` directory.

```
ln -s config/compilers.yaml   ./spack/etc/spack/compilers.yaml
```

The config.yaml file has settings for where to save the cache, which needs to be set somewhere on the work folder. 

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

Typing in `spack load` will not be loading the modules. Thus the Cray compiler is not aware that a library has been loaded. Stantard environment paths are updated, such as PATH or LD_LIBRARY_PATH. 
For instance in a GNU programming environment.

```bash
lparisi@uan01:/work/z19/z19/lparisi/spack> echo $LD_LIBRARY_PATH
/opt/cray/pe/gcc/11.2.0/snos/lib64:/opt/cray/pe/papi/6.0.0.17/lib64:/opt/cray/libfabric/1.12.1.2.2.0.0/lib64
lparisi@uan01:/work/z19/z19/lparisi/spack> spack load hdf5
lparisi@uan01:/work/z19/z19/lparisi/spack> echo $LD_LIBRARY_PATH
/opt/cray/pe/gcc/11.2.0/snos/lib64:/opt/cray/pe/papi/6.0.0.17/lib64:/opt/cray/libfabric/1.12.1.2.2.0.0/lib64:/opt/cray/pe/hdf5-parallel/1.12.2.1/gnu/9.1/lib
lparisi@uan01:/work/z19/z19/lparisi/spack> module list 2>&1  | grep -i --color hdf5
lparisi@uan01:/work/z19/z19/lparisi/spack> 
```

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