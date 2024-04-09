# Spack
This repo contains the configuration, build and run instructions for the spack installation on Archer2.


## Using spack

### Loading spack
The modules are installed as development modules on archer2.

```bash
module use /work/y07/shared/archer2-lmod/apps/dev
```

The user spack module can be loaded with 

```bash
module load spack
```
while the central cse module ( for installing centraly supported packages ) can be loaded with 

```bash
module load spack-epcc
```
You will also need to source the spack environment with 

```bash
source $SPACK_ROOT_EPCC/source.sh
```

### Useful commands

`spack find`:  view installed packages. Se `spack find -h` for options.
`spack install ${SPEC}` : to install a specifick package name.
`spack compilers` : show availabe compilers
`spack list ` : shows all packages available in the repository

### Creating packages

A scaffold for a spack package can be created by typing
```
spack create --force --name hello_world https://github.com/lucaparisi91/hello_world/archive/refs/tags/v1.0.tar.gz
```
A few examples can be found in the `custom_packages` subdirectory.


## Installation of spack

Fir set the environmet variable to the folder where you want to install spack

```bash
export `${SPACK_ROOT_EPCC}=... root directory of the spack installation ...`
```

Then install spack with

```bash
wget https://github.com/spack/spack/archive/refs/tags/v0.21.2.tar.gz
tar -zxvf v0.21.2.tar.gz
```

This will create a folder called spack-v0.21.2 in your installation directory. Set an environment variable which points to this folder .

```bash
export `${SPACK_ROOT}=${SPACK_ROOT_EPCC}/spack-v0.21.2`
```

You can now use `source $SPACK_ROOT/share/spack/setup-env.sh` to setup the spack environment. 

### Configuration of spack

These repo contsin configurations for two installations of spack

1. A centrally available installation. All packages installed trough spack with this config will be saved in a centralled saved directory on `y07` . This installation is meant to be used by cse only to provide centrally installed packages to other users. The installation can be loaded using `module load spack-epcc`. The configuration files are present in the `central_install` subdirectory.

2. A user installation. All packages installated trough spack will be installed in a local directory for the user. By default this will be in `/work/<project>/<project>/<user>/.spack` . This installation points to the central installation and all packes installed in the central installation are available as well. The configuration files are present in the `user_install` subdirectory.

For installing the central installation, you will need to copy the contents of the files to `${SPACK_ROOT_EPCC}` and the content of `config` subdirectory to `${SPACK_ROOT}/etc/spack`.

```bash
cp -r  config/*.yaml ${SPACK_ROOT}/etc/spack
cp -r archer2repo ${SPACK_ROOT_EPCC}
cp source.sh ${SPACK_ROOT_EPCC}
cp -r environments ${SPACK_ROOT_EPCC}
```

To set the proper environment, source the `source.sh` file

```bash
source ${SPACK_ROOT_EPCC}/source.sh
```

These will make use of the `${SPACK_ROOT_EPCC}` and `${SPACK_ROOT}` environment variables.

In order to create the user installation repeat the whole installation and configuration process, but in a different `${SPACK_ROOT_EPCC}` folder and use the `user_install` configuration files instead of `central_install`.
You will also need to point the user installation to the central installation by modifying the `upstreams.yaml` file in the `user_install/config` subdirectory.



These configuration can be overriden by the user by calling spack with `-C custom_config_folder` option, where `custom_config_folder` is a directory containing `.yaml` configuration files for spack.




## Verified software
The current status of spack packages.

software | spack package | builds | run  | compiler
------- | --------| -------- | --------- | -------- |
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
quantum espresso | Yes | Yes ( patched ) | Yes| gnu
vasp | yes | | |
crystal | no  | | |
petsc | | |
scotch | Yes | |
trilinos | | |
parmetis | | |
pytorch | Yes | no ( metadata generation failed) | | gnu |
tensorflow | | | | |

