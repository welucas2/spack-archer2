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


class HelloWorld(MakefilePackage):
    """ Hello World test package """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/lucaparisi91/hello_world"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    version("1.0", sha256="a85ab0fd5a09caf8b214ac3041c0e69fb3deb098b9a6464d1eff6cfe4d8e0510", url = "https://github.com/lucaparisi91/hello_world/archive/refs/tags/v1.0.tar.gz")


    version("2.0", sha256= "91dd03780d2cd9cf6c8905bea48c6f41ab160ba48555e642e54cf4818b6361d4", url = "https://github.com/lucaparisi91/hello_world/archive/refs/tags/v2.0.tar.gz", 
     )

    variant(
        "mpi", default=False, description="Builds a MPI Hello World! example"
    )
    depends_on("mpi", when="+mpi")


    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter("Makefile")
        # makefile.filter("CC = .*", "CC = cc")
        env['PREFIX'] = prefix 

        if "+mpi" in self.spec:
            env["MPI"]="TRUE"
            env["CXX"]="mpicxx"
            env["CC"]="mpicc"
            env["FC"]="mpifort"