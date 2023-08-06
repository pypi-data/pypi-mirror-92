import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_easyDL",
    version="0.0.8",
    description="easyDL - Where Deep learning is meant to be easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "Operating System :: OS Independent",
    ],
    url="https://github.com/ThisisAEmam/easyDL",
    author="easyDL team",
    author_email="abdoemamofficial@gmail.com",

    install_requires = [
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "opencv-python",
        "idx2numpy",
        "tqdm",
        ],
    python_requires='>=3.6',
    )
