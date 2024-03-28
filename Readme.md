## Installation of spack
You can install spack by typing
```
git clone -c feature.manyFiles=true https://github.com/spack/spack.git
```
and then can use `source ./spack/share/spack/setup-env.sh` to setup the spack environment.

to see the available spack compilers.

## Configuration of spack
Using `spack config add concretizer:reuse:false` spack will build from source instead of downloading binaries, even if available.
We put configuration files in the `config` directory.
The directory containing configuration files can be specified with the `-C` option. For instance you could type the command
```
spack -C $CONFIG_DIR compilers
```
Alternatively you can copy the configuration files in `config` to `spack/etc/spack`. This will override builtin configuration files,
but not user configuration files.
```
source source.sh
```
You will need to edit `SPACK_ROOT_EPCC`, the path of this directory, and `SPACK_ROOT`, the path where spack is installed in the `source.sh` file.

Bootstrap files are saved in the home directory. This can be changed with the command `spack bootstrap root ${BOOTSTRAP_FOLDER}`.


### Compilers
Gnu, amd and cray compilers were configured with the bare compilers, instead of pointing to the Cray wrappers.
This is because spacks would call a wrapper on the Cray wrapper and flags can get get mangled. Using the bare compilers avoids the problem.
The `compilers.yaml` file contains the compiler configuration.
### Libraries
The Cray libraries for MPI,BLAS, LAPACK, HDF5, FFTW, NETCDF have been configured in the `package.json` configuration file.
Typing in `spack load` will not be loading the cray modules. Thus the Cray compiler is not aware that a library has been loaded. However stantard environment paths are updated, such as `PATH` or `LD_LIBRARY_PATH`. 
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
`spack install ${SPEC}` to install a specifick package name. A list of packages which can be installed with spack can be obtained with `spack list`.

### Creating packages

A scaffold for a spack package can be created by typing
```
spack create --force --name hello_world https://github.com/lucaparisi91/hello_world/archive/refs/tags/v1.0.tar.gz
```
A few examples can be found in the `packages` subdirectory.

### CMake 

I have prepared a patched version of CMake. This version should be able to find Blas and Lapack. The patch will only work on Cray systems.

## Verified software
software | spack package | builds | run  | compiler
------- | --------| -------- | --------- |
CASTEP | No  | | |
Code_Saturne | No | | |
CP2K | Yes | Yes | |
Py-ChemShell/Tcl-ChemShell | | | |
FHI-aims | No | | |
Gromacs | Yes | Yes | | gnu
Lammps |Yes | Yes | | gnu
namd | Yes | No ( manual fetching of source code required) | | | 
nektar++ | | | | |
nemo | No | | | | 
nwchem | Yes | | | |
onetep | no  | | | |
openfoam | Yes | Yes | | |
quantum espresso | Yes | Yes ( patched ) | | | gnu
vasp | yes | | |
crystal | no  | | |
petsc | | |
scotch | Yes | |
trilinos | | |
parmetis | | |
pytorch | Yes | no ( metadata generation failed) | | |
tensorflow | | | | |
