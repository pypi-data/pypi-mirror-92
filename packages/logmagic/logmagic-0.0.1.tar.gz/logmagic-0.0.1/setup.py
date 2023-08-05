import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logmagic",
    version="0.0.1",
    author="Katkam Nitin Narsing Reddy",
    author_email="redknitin@gmail.com",
    description="Log helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nitinkatkam/logmagic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
