from distutils.core import setup
import py2exe

setup(
    console=['enigma.py'],
    options={ 
                'py2exe': 
                { 
                    'includes': []
                }
            },
    )