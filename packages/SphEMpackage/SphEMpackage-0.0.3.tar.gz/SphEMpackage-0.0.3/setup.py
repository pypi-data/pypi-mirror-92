import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SphEMpackage", # Replace with your own username
    version="0.0.3",
    author="Mahmoud Elzouka",
    author_email="mhmodzoka@gmail.com",
    description="Trying to package all Python codes with dependencies here",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhmodzoka/SphEM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

# pypi-AgEIcHlwaS5vcmcCJDJmZjEzZjYwLWNiZjktNDNiNy1iODBhLTJiZjgwYmIwYzZhMgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgnKGCZDSiTNIl41Umt6diAgPQ49KAgp7gF0ghSxChMC4
