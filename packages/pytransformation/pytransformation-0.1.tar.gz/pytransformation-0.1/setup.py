from setuptools import setup
import os


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = os.path.join(thelibFolder, 'requirements.txt')
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = list(f.read().splitlines())

setup(name="pytransformation",
      install_requires=install_requires,
      packages=['pytransformation'],
      version='0.1',
      license='GPLv3',
      description='Source code transformations for cross-compilation.',
      author='Dylan Fox',
      author_email='dylan.fox@colorado.edu',
      url='https://github.com/Dyfox100/pytransformation',
      download_url='https://github.com/Dyfox100/pytransformation/archive/v0.1.tar.gz',  # noqa: E251, E501
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
      ])
