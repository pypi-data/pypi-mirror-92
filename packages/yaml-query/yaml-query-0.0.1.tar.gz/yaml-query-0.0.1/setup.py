import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="yaml-query",
    version="0.0.1",
    author="kubasobon",
    author_email="wtty.fool@gmail.com",
    description="yaml query library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kubasobon/yaml-query",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
