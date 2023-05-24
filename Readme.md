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

### Installing Cray libraries
- MPI
- BLAS 
- LAPACK
- HDF5
- FFTW
- NETCDF

## Using spack

`spack find`:  to view installed packages. Se `spack find -h` for options.

### Creating packages

A template for a spack package can be created by typing
```
spack create --force --name hello_world https://github.com/lucaparisi91/hello_world/archive/refs/tags/v1.0.tar.gz
```