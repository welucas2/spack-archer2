## Configuration of spack

git clone -c feature.manyFiles=true https://github.com/spack/spack.git
source ./spack/share/spack/setup-env.sh

spack config add concretizer:reuse:false # will build from source instead of downloading the binaries.

We put configuration files in `spack/spack/etc/spack`. 
```
mv ~/.spack/linux/compilers.yaml ./spack/spack/etc/spack.
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

You can use `spack find` to view installed packages. Se `spack find -h` for options.