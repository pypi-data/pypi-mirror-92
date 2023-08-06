import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Nipo",
    version="0.0.1",
    author="Harsha Addanki",
    author_email="harsha7addanki@gmail.com",
    description="Awesome Wsgi Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harsha7addanki/Nipo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)