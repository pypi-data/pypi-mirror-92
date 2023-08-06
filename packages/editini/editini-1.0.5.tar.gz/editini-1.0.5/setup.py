import setuptools

setuptools.setup(
    name="editini",
    version="1.0.5",
    author="Penguin0093",
    author_email="0093penguin@gmail.com",
    description="It is easy to write and read "+".ini"+".  ",
    url="",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    long_description=open("README.rst","r",encoding="utf-8").read()
)
