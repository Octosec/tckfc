tckfc
=====

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

    mkdir mnt
    cp a.pdf keys/
    cp b.doc keys/
    cp c.txt keys/
    cp d.jpg keys/
    cp e.gif keys/
    python tckfc.py keys/ encrypted.img 123456 mnt/




[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/Octosec/tckfc/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

