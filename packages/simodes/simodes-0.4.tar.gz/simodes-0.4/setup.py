from setuptools import setup

setup(
      name='simodes',

      version='0.4',
      description='Platform for connection of ODE and DES based simulations',
      url='http://github.com/hrbolek/simodes',
      author='Profesor Hrbolek',
      author_email='profesor@hrbolek.cz',
      license='MIT',
      packages=['simodes'],
      install_requires=[
          'scipy'
      ],      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
      ],
      zip_safe=False)