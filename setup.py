from setuptools import setup, find_packages

setup(
    name='fastapi-modelrouter',
    version='0.0.2',
    license='MIT',
    description='fastAPI CRUD-Router for SqlAlchemy models',
    author="Uwe Windt",
    author_email='uwe.windt@windisoft.de',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/UweWindt/fastapi-modelrouter',
    keywords='fastapi router sqlalchemy',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'sqlalchemy',
    ],

)
