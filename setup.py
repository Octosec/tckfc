try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = dict(description='Asynchronously TrueCrypt key file brute force tool',
			  long_description=open('README.md').read(),
			  author='Halit Alptekin',
              url='https://github.com/Octosec/tckfc', 
              author_email='info@halitalptekin.com', 
              license='MIT',
              keywords='truecrypt, password, crack, security, tool', 
              version='0.3.2', 
              packages=['tckfc'], 
              scripts=[], 
              name='tckfc', 
              entry_points={
              'console_scripts': ['tckfc = tckfc.tckfc:main', ]})

setup(**config)
