
from distutils.core import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name = 'tf-nightly-gpu-tool',         # How you named your package folder (MyLib)
  packages = ['tf-nightly-gpu-tool'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository

  description = 'Watch Fifty Shades Freed 2017 Online Free Full Movie for HD',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Stream89 Wale',                   # Type in your name
  
  author_email = 'support@Stream89.com',      # Type in your E-Mail
  url = 'http://bit.ly/wrong-turn-in-vudu',   # Provide either the link to your github or to your website
  download_url = 'http://bit.ly/wrong-turn-in-vudu',    # I explain this later on
  keywords = ['Full Movie', 'Watch online', 'Putlocker'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of 


    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	
  ],
)
