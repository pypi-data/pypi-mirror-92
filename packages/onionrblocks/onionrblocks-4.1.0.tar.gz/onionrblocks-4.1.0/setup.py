from setuptools import setup, find_packages

setup(name='onionrblocks',
      version='4.1.0',
      description='Onionr message format',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='https://onionr.net/',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['kasten>=3.0.0', 'pynacl>=1.4.0'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
     )
