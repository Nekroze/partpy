Performance
-----------

``partpy`` is written with ``Cython`` support through .pxd files and can be
compiled for extra speed. If you do not want to use ``Cython`` simply install
it from the source with ``Cython`` uninstalled.

If however you use ``pip`` or ``easy_install`` or something similar ``Cython``
is marked a dependency and must be installed.

``partpy`` is tested without compilation on python{2.6, 2.7, 3.2} and the latest
pypy stable release. All these platforms are also tested with cython compilation
except for python{2.6}. As an additional bonus ``partpy`` is also tested for
rpython translation. This means that the pypy rpython translation toolchain
can compile ``partpy`` making it useable in very fast interpreters/VM's using
pypy toolchain that can also provide a JIT compiler for free.

All of the compilation and usage options are designed to allow for maximum
flexability while also allowing maximum performance and usage.
