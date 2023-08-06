import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="javelin",
    version="0.0.1",
    author="Jeremy Kanovsky",
    author_email="kanovsky.jeremy@gmail.com",
    description="A small micro-controller commander",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xJeremy/javelin",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",],
)
