import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rangealert",
    version="0.0.1",
    author="Jonathan Leon",
    author_email="jonleonaustin@gmail.com",
    description="Range bound trading screener",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonleonATX/range_trading_alert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
