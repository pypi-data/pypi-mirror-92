import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bsoder", # Replace with your own username
    version="0.0.1",
    author="Alex Zaslavskis",
    author_email="sahsariga111@gmail.com",
    description="A small example package",
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