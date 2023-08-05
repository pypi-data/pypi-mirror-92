from distutils.core import setup

try:
  with open("README.md","r") as fh:
    long_description = fh.read()
except:
  long_description = 'OOP Learning Example by lidm0707'

setup(
  name = 'testlearing04UncelShcool',         # How you named your package folder (MyLib)
  packages = ['testlearing04UncelShcool'],   # Chose the same as "name"
  version = '0.0.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'OOP Learning Example by lidm0707',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type = "text/markdown",
  author = 'lidm0707',                   # Type in your name
  author_email = 'lightdemon17@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/lidm0707/BBSic-oop',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lidm0707/BBSic-oop/archive/v_00.tar.gz',    # I explain this later on
  keywords = ['OOP', 'THAI', 'PYTHON'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)