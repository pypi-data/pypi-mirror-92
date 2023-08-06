import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="legmath", 
    version="1.0",
    author="Example Author",
    author_email="throwawayemail49572@gmail.com",
    description="legacy random",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JezBurch1984/xrandom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
