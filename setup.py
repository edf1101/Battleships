import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="battleships-edf1101",
    version="1.6",
    author="Student 130003140",
    author_email="ef494@exeter.ac.uk",
    description="2023 ECM1400 Coursework - Battleships",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edf1101/Battleships",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['static/images/*', 'templates/*', '*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.4",
    install_requires=["Flask==3.0.0", "numpy==1.26.2"]
)