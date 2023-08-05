import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="mokujin",
        version="2.0",
        author="dynazero",
        author_email="garcia.jimmyj@gmail.com",
        description="frame data bot for our discord channel",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dynazero/mokujin",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6',

        )