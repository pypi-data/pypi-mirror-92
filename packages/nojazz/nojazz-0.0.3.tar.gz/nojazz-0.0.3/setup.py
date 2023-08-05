import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    description = long_description.split("\n")[2]

setuptools.setup(
    name="nojazz",
    version="0.0.3",
    author="NapsterInBlue",
    author_email="napsterinblue@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NapsterInBlue/nojazz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas"],
)