from spack import *

class Wxpropgrid(Package):
    """wxPropertyGrid is a property sheet control for wxWidgets. In other words, it is a specialized two-column grid for editing properties such as strings, numbers, flagsets, string arrays, and colours."""
    homepage = "http://wxpropgrid.sourceforge.net/"
    url      = "http://prdownloads.sourceforge.net/wxpropgrid/wxpropgrid-1.4.15-src.tar.gz"

    versions = { '1.4.15' : 'f44b5cd6fd60718bacfabbf7994f1e93', }

    depends_on("wx")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--with-wxdir=%s" % spec['wx'].prefix.bin, "--enable-unicode")

        make()
        make("install")

