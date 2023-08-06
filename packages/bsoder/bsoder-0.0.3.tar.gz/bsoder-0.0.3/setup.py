import setuptools

long_description="""
# Bsoder
Simple Lib that will cause bsod on you pc 

[Docs](https://alex5250.github.io/bsoder/)

"""

setuptools.setup(
    name="bsoder", # Replace with your own username
    version="0.0.3",
    author="Alex Zaslavskis",
    author_email="sahsariga111@gmail.com",
    description="A small example package for cause BSOD`s on Windows PC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex5250/bsoder",
	download_url = 'https://github.com/alex5250/bsoder/releases/download/v0.0.1/bsoder.tar',    # I explain this later on
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)