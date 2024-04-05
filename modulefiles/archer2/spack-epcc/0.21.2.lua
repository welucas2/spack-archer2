help([[
Spack 0.21.2
==============
Spack is a package management tool for hpc.

- Installed by: L. Parisi, EPCC"
   - Date: 28 March 2024\n"
]])

local pkgBase = "/mnt/lustre/a2fs-nvme/work/y07/shared/spack/0.21.2/spack-epcc"

setenv("SPACK_ROOT_EPCC", pkgBase)
setenv("SPACK_ROOT",pathJoin(pkgBase,"spack-0.21.2"))
family("spack")
