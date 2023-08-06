from distutils.core import setup
setup(
  name = 'quick_dag',         # How you named your package folder (MyLib)
  packages = ['quick_dag'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Create quick dags',   # Give a short description about your library
  author = 'Stefan Krone',                   # Type in your name
  author_email = 'stefan.krone@yahoo.de',      # Type in your E-Mail
  url = 'https://github.com/kroone/quick_dag',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kroone/quick_dag/archive/0.01.tar.gz',    # I explain this later on
  keywords = ['dag'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'matplotlib',
          'causalgraphicalmodels',
          'daft'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)