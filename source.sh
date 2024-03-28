export SPACK_ROOT_EPCC=/work/z19/z19/lparisi/spack/spack
export SPACK_ROOT=/work/z19/z19/lparisi/spack/spack/spack
export SPACK_USER_CACHE_PATH=/work/$(id -gn)/$(id -gn)/$(id -un)/spack/spack/.spack

source $SPACK_ROOT/share/spack/setup-env.sh
export PATH=$SPACK_ROOT_EPCC/bin:$PATH
