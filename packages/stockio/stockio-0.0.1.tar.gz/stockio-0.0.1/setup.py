from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Stock Market Data Lake'
LONG_DESCRIPTION = 'Combines Deep Learning and Apis'

setup(
        name="stockio", 
        version=VERSION,
        author="Christopher Bradley",
        author_email="declarationcb@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
				python_requires='>=3',
        install_requires=[],
        keywords=['python', 'deep learning', 'stocks', 'ai'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
        ]
)