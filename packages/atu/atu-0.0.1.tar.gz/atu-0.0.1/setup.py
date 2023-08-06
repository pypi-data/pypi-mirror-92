import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atu", 
    version="0.0.1",
    author="atutongxue",
    author_email="atutongxue@example.com",
    description="This is description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atutongxue/atu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)