import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mfperfquery", # Replace with your own username
    version="1.0.2",
    author="Aditya Raghavan",
    author_email="aditya14920251@gmail.com",
    description="Python library for extracting certain performance parameters of Mutual Funds in India from https://moneycontrol.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Mutual Funds, Funds, Moneycontrol, Stock",
    url="https://github.com/adraghav/MFPerfQuery",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)