# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install hello-world
#
# You can edit this file again by typing:
#
#     spack edit hello-world
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *

class Benchio(CMakePackage):
    """ Benchio: simple benchmark to test IO performance """

    homepage = "https://github.com/lucaparisi91/benchio"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    version("1.0.5",  sha256="7e6cfb0c13f0b9c8fbab877ca1350bf41a41cb5fa3f557f52f72d1d13127d842", url = "https://github.com/lucaparisi91/benchio/archive/refs/tags/1.0.5.tar.gz")

    depends_on("mpi")

    variant(
        "hdf5", default=False, description="Performs an HDF5 write performance test"
    )
    variant(
        "netcdf", default=False, description="Performs a NETCDF write performance test"
    )
    variant(
        "adios2", default=False, description="Performs a ADIOS2 write performance test"
    )

    depends_on("hdf5+mpi",when="+hdf5")
    depends_on("netcdf-fortran",when="+netcdf")
    depends_on("adios2",when="+adios2")
    

    def cmake_args(self):

        args=[]
        
        if "+netcdf" in self.spec:
            args = args + [    
               "-DUSE_NETCDF=TRUE"
            ]

        if "+hdf5" in self.spec:
            args = args + [    
               "-DUSE_HDF5=TRUE"
            ]
        if "+adios2" in self.spec:
            args = args + [    
               "-DUSE_ADIOS2=TRUE"
            ]
        

        return args


    