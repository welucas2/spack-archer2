# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Castep(CMakePackage):
    """CASTEP is a software package to calculate the properties of materials.
    It is based on quantum mechanics, in a form known as density functional
    theory, and can simulate a wide range of materials proprieties including
    energetics, structure at the atomic level, vibrational properties, and
    many experimental characterisation methods, such as infra-red and Raman
    spectra, NMR, and core-level spectra.
    """

    homepage = "https://www.castep.org/home"
    manual_download = True
    url = "file://{0}/castep-24.1.tar.gz".format(os.getcwd())

    maintainers("NMannall")

    version("24.1", sha256="97d77a4f3ce3f5c5b87e812f15a2c2cb23918acd7034c91a872b6d66ea0f7dbb")

    depends_on("cray-fftw")
    depends_on("python")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("libxc")

    patch("24.1.patch", when="@24.1")
    patch("libxc_mod.patch", when="@24.1")

    def url_for_version(self, version):
        return "file://{0}/castep-{1}.tar.gz".format(
            os.getcwd(), version
        )

    def cmake_args(self):
        args = [
            self.define("BUILD", "fast"),
            self.define("COMMS_ARCH", "mpi"),
            self.define("FFT", "fftw3"),
            self.define("WITH_LIBXC", True)
        ]
        return args

