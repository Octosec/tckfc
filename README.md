tckfc
=====

[![Latest Version](https://img.shields.io/pypi/v/tckfc.svg)](https://pypi.python.org/pypi/tckfc/)
[![Downloads](https://img.shields.io/pypi/dm/tckfc.svg)](https://pypi.python.org/pypi/tckfc/)
[![Download format](https://img.shields.io/pypi/format/tckfc.svg)](https://pypi.python.org/pypi/tckfc/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/tckfc.svg)](https://pypi.python.org/pypi/tckfc/)
[![License](https://img.shields.io/pypi/l/tckfc.svg)](https://pypi.python.org/pypi/tckfc/)

This tool seeks asynchronously TrueCrypt key file using combinations of provided key files with provided password.

Installation
============
    pip install tckfc

Usage
=====

``tckfc [-h] [-c [COMBINATION]] keyfiles tcfile password``

  * **keyfiles:** Possible key files directory
  * **tcfile:** TrueCrypt encrypted file
  * **password:** Password for TrueCrypt file

Example
=======

    cp a.pdf keys/
    cp b.doc keys/
    cp c.txt keys/
    cp d.jpg keys/
    cp e.gif keys/
    python tckfc.py keys/ encrypted.img 123456

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/Octosec/tckfc/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

