import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fish-all",
    version="0.0.3",
    author="Valter Daugberg",
    author_email="valteryde@hotmail.com",
    description="This projekt is made by an amateour and is made for small uses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    data_files=['fish/gui/left.png', 'fish/gui/right.png']
)