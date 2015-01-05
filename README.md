tckfc
=====

This tool seeks TrueCrypt key file using combinations of provided key files with known password.

Usage
=====

``python tckfc.py [-h] [-c [COMBINATION]] keyfiles tcfile password mountpoint``

  * **keyfiles:** Possible key files directory
  * **tcfile:** TrueCrypt encrypted file
  * **password:** Password for TrueCrypt file
  * **mountpoint:** Mount point

Example
=======

    mkdir mnt
    cp a.pdf keys/
    cp b.doc keys/
    cp c.txt keys/
    cp d.jpg keys/
    cp e.gif keys/
    python tckfc.py keys/ encrypted.img 123456 mnt/


