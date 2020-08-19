from setuptools import setup, find_packages

setup(name='gym_circuit',
      packages=find_packages(),
      include_package_data=True,
      version='0.0.1',
      install_requires=[
          'gym',
          'pillow',
          'noise'
      ]
)