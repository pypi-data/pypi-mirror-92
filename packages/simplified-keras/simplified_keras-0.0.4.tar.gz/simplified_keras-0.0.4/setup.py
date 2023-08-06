import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simplified_keras',
    version='0.0.4',
    author="Albert Lis",
    author_email="albert.lis.1996@gmail.com",
    description="Common used code in Keras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertlis/simplified-keras",
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib >= 3.0",
        "keras >= 2.0", 
        "numpy >= 1.0",
        "tensorflow >= 2.0",
        "seaborn >= 0.10",
        "pandas >= 1.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
