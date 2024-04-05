# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import spack.build_environment
from spack.package import *


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """

    homepage = "https://www.cmake.org"
    url = "https://github.com/Kitware/CMake/releases/download/v3.19.0/cmake-3.19.0.tar.gz"
    git = "https://gitlab.kitware.com/cmake/cmake.git"

    maintainers("alalazo")

    tags = ["build-tools", "windows"]

    executables = ["^cmake[0-9]*$"]

    version("master", branch="master")
    version("3.26.3", sha256="bbd8d39217509d163cb544a40d6428ac666ddc83e22905d3e52c925781f0f659")
    
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516
    patch("cmake-revert-findmpi-link-flag-list.patch", when="@3.15.0")
    
    patch("blas-cray.patch", when="@3.26.3")
    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873
    patch("cmake-macos-add-coreservices.patch", when="@3.11.0:3.13.3")

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    patch(
        "fix-xlf-ninja-mr-4075.patch",
        sha256="42d8b2163a2f37a745800ec13a96c08a3a20d5e67af51031e51f63313d0dedd1",
        when="@3.15.5",
    )

    depends_on("ninja", when="platform=windows")

    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant("ownlibs", default=True, description="Use CMake-provided third-party libraries")
    variant("qt", default=False, description="Enables the build of cmake-gui")
    variant(
        "doc",
        default=False,
        description="Enables the generation of html and man page documentation",
    )
    variant(
        "ncurses",
        default=sys.platform != "win32",
        description="Enables the build of the ncurses gui",
    )

    # See https://gitlab.kitware.com/cmake/cmake/-/issues/21135
    conflicts(
        "%gcc platform=darwin",
        when="@:3.17",
        msg="CMake <3.18 does not compile with GCC on macOS, "
        "please use %apple-clang or a newer CMake release. "
        "See: https://gitlab.kitware.com/cmake/cmake/-/issues/21135",
    )

    # Vendored dependencies do not build with nvhpc; it's also more
    # transparent to patch Spack's versions of CMake's dependencies.
    conflicts("+ownlibs %nvhpc")

    # Use Spack's curl even if +ownlibs, since that allows us to make use of
    # the conflicts on the curl package for TLS libs like OpenSSL.
    # In the past we let CMake build a vendored copy of curl, but had to
    # provide Spack's TLS libs anyways, which is not flexible, and actually
    # leads to issues where we have to keep track of the vendored curl version
    # and its conflicts with OpenSSL.
    depends_on("curl")

    # When using curl, cmake defaults to using system zlib too, probably because
    # curl already depends on zlib. Therefore, also unconditionaly depend on zlib.
    depends_on("zlib")

    with when("~ownlibs"):
        depends_on("expat")
        # expat/zlib are used in CMake/CTest, so why not require them in libarchive.
        depends_on("libarchive@3.1.0: xar=expat compression=zlib")
        depends_on("libarchive@3.3.3:", when="@3.15.0:")
        depends_on("libuv@1.0.0:1.10", when="@3.7.0:3.10.3")
        depends_on("libuv@1.10.0:1.10", when="@3.11.0:3.11")
        depends_on("libuv@1.10.0:", when="@3.12.0:")
        depends_on("rhash", when="@3.8.0:")

    depends_on("qt", when="+qt")
    depends_on("ncurses", when="+ncurses")

    with when("+doc"):
        depends_on("python@2.7.11:", type="build")
        depends_on("py-sphinx", type="build")

    # TODO: update curl package to build with Windows SSL implementation
    # at which point we can build with +ownlibs on Windows
    conflicts("~ownlibs", when="platform=windows")
    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch("intel-c-gnu11.patch", when="@3.6.0:3.6.1")

    # Cannot build with Intel again, should be fixed in 3.17.4 and 3.18.1
    # https://gitlab.kitware.com/cmake/cmake/-/issues/21013
    patch("intel-cxx-bootstrap.patch", when="@3.17.0:3.17.3,3.18.0")

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch("nag-response-files.patch", when="@3.7:3.12")

    # Cray libhugetlbfs and icpc warnings failing CXX tests
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4698
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4681
    patch("ignore_crayxc_warnings.patch", when="@3.7:3.17.2")

    # The Fujitsu compiler requires the '--linkfortran' option
    # to combine C++ and Fortran programs.
    patch("fujitsu_add_linker_option.patch", when="%fj")

    # Remove -A from the C++ flags we use when CXX_EXTENSIONS is OFF
    # Should be fixed in 3.19.
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025
    patch("pgi-cxx-ansi.patch", when="@3.15:3.18")

    # Adds CCE v11+ fortran preprocessing definition.
    # requires Cmake 3.19+
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5882
    patch(
        "5882-enable-cce-fortran-preprocessing.patch",
        sha256="b48396c0e4f61756248156b6cebe9bc0d7a22228639b47b5aa77c9330588ce88",
        when="@3.19.0:3.19",
    )

    conflicts("+qt", when="^qt@5.4.0")  # qt-5.4.0 has broken CMake modules

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts("%intel", when="@3.11.0:3.11.4")
    conflicts("%intel@:14", when="@3.14:", msg="Intel 14 has immature C++11 support")

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v3.21/cmake-3.21.2-windows-x86_64.zip",
        checksum="213a4e6485b711cb0a48cbd97b10dfe161a46bfe37b8f3205f47e99ffec434d2",
        placement="cmake-bootstrap",
        when="@3.0.2: platform=windows",
    )

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip",
        checksum="8b9b520f3372ce67e33d086421c1cb29a5826d0b9b074f44a8a0304e44cf88f3",
        placement="cmake-bootstrap",
        when="@:2.8.10.2 platform=windows",
    )

    phases = ["bootstrap", "build", "install"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"cmake.*version\s+(\S+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.compiler.name == "fj":
            cxx11plus_flags = (self.compiler.cxx11_flag, self.compiler.cxx14_flag)
            cxxpre11_flags = self.compiler.cxx98_flag
            if any(f in flags for f in cxxpre11_flags):
                raise ValueError("cannot build cmake pre-c++11 standard")
            elif not any(f in flags for f in cxx11plus_flags):
                flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def bootstrap_args(self):
        spec = self.spec
        args = []
        self.generator = make

        # The Intel compiler isn't able to deal with noinline member functions of
        # template classes defined in headers.  As such it outputs
        #   warning #2196: routine is both "inline" and "noinline"
        # cmake bootstrap will fail due to the word 'warning'.
        if spec.satisfies("%intel@:2021.6.0"):
            args.append("CXXFLAGS=-diag-disable=2196")

        if self.spec.satisfies("platform=windows"):
            args.append("-GNinja")
            self.generator = ninja

        if not sys.platform == "win32":
            args.append("--prefix={0}".format(self.prefix))

            jobs = spack.build_environment.get_effective_jobs(
                make_jobs,
                parallel=self.parallel,
                supports_jobserver=self.generator.supports_jobserver,
            )
            if jobs is not None:
                args.append("--parallel={0}".format(jobs))

            if "+ownlibs" in spec:
                # Build and link to the CMake-provided third-party libraries
                args.append("--no-system-libs")
            else:
                # Build and link to the Spack-installed third-party libraries
                args.append("--system-libs")

                if spec.satisfies("@3.2:"):
                    # jsoncpp requires CMake to build
                    # use CMake-provided library to avoid circular dependency
                    args.append("--no-system-jsoncpp")

            # Whatever +/~ownlibs, use system curl.
            args.append("--system-curl")

            if "+qt" in spec:
                args.append("--qt-gui")
            else:
                args.append("--no-qt-gui")

            if "+doc" in spec:
                args.append("--sphinx-html")
                args.append("--sphinx-man")

            # Now for CMake arguments to pass after the initial bootstrap
            args.append("--")
        else:
            args.append("-DCMAKE_INSTALL_PREFIX=%s" % self.prefix)

        args.extend(
            [
                f"-DCMAKE_BUILD_TYPE={self.spec.variants['build_type'].value}",
                # Install CMake correctly, even if `spack install` runs
                # inside a ctest environment
                "-DCMake_TEST_INSTALL=OFF",
                f"-DBUILD_CursesDialog={'ON' if '+ncurses' in spec else 'OFF'}",
            ]
        )

        # Make CMake find its own dependencies.
        rpaths = spack.build_environment.get_rpaths(self)
        prefixes = spack.build_environment.get_cmake_prefix_path(self)
        args.extend(
            [
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON",
                "-DCMAKE_INSTALL_RPATH={0}".format(";".join(str(v) for v in rpaths)),
                "-DCMAKE_PREFIX_PATH={0}".format(";".join(str(v) for v in prefixes)),
            ]
        )

        return args

    def cmake_bootstrap(self):
        exe_prefix = self.stage.source_path
        relative_cmake_exe = os.path.join("cmake-bootstrap", "bin", "cmake.exe")
        return Executable(os.path.join(exe_prefix, relative_cmake_exe))

    def bootstrap(self, spec, prefix):
        bootstrap_args = self.bootstrap_args()
        if sys.platform == "win32":
            bootstrap = self.cmake_bootstrap()
            bootstrap_args.extend(["."])
        else:
            bootstrap = Executable("./bootstrap")
        bootstrap(*bootstrap_args)

    def build(self, spec, prefix):
        self.generator()

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Some tests fail, takes forever
        self.generator("test")

    def install(self, spec, prefix):
        self.generator("install")

        if spec.satisfies("%fj"):
            for f in find(self.prefix, "FindMPI.cmake", recursive=True):
                filter_file("mpcc_r)", "mpcc_r mpifcc)", f, string=True)
                filter_file("mpc++_r)", "mpc++_r mpiFCC)", f, string=True)
                filter_file("mpifc)", "mpifc mpifrt)", f, string=True)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before cmake packages's install() methods."""

        module.cmake = Executable(self.spec.prefix.bin.cmake)
        module.ctest = Executable(self.spec.prefix.bin.ctest)

    @property
    def libs(self):
        """CMake has no libraries, so if you ask for `spec['cmake'].libs`
        (which happens automatically for packages that depend on CMake as
        a link dependency) the default implementation of ``.libs` will
        search the entire root prefix recursively before failing.

        The longer term solution is for all dependents of CMake to change
        their deptype. For now, this returns an empty set of libraries.
        """
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])

    def run_version_check(self, bin):
        """Runs and checks output of the installed binary."""
        exe_path = join_path(self.prefix.bin, bin)
        if not os.path.exists(exe_path):
            raise SkipTest(f"{exe} is not installed")

        exe = which(exe_path)
        out = exe("--version", output=str.split, error=str.split)
        assert f"version {self.spec.version}" in out

    def test_ccmake(self):
        """check version from ccmake"""
        self.run_version_check("ccmake")

    def test_cmake(self):
        """check version from cmake"""
        self.run_version_check("cmake")

    def test_cpack(self):
        """check version from cpack"""
        self.run_version_check("cpack")

    def test_ctest(self):
        """check version from ctest"""
        self.run_version_check("ctest")
