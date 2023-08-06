from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'KnowBe4 API Python Wrapper'
LONG_DESCRIPTION = 'KnowBe4 API Python Wrapper. Supports pagation'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="KnowBe4Wrapper", 
        version=VERSION,
        author="Chase Geis",
        author_email="<Chasegeis@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'KnowBe4', 'KnowBe4 API', 'API', 'KnowBe4 Wrapper', 'KnowBe4 Python Wrapper'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)