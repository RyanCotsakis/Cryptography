from distutils.core import setup
import py2exe

setup(
    console=['encoder_1.1.py'],
    options={ 
                'py2exe': 
                { 
                    'includes': ['docx', 'PIL', 'lxml.etree', 'lxml._elementpath', 'gzip']
                }
            },
    packages=[
          'C:\Users\Ryan\Anaconda2\Lib\site-packages\docx'
          ],
    package_data={
          'C:\Users\Ryan\Anaconda2\Lib\site-packages\docx': [
              '_rels/*',
              'docProps/*',
              'word/theme/*.xml',
              'word/*.xml'
          ],
      },
    )