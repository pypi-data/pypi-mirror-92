import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='EasyNN',
    version='0.0.3',
    description='Currently Testing',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    url="https://github.com/danielwilczak101/EasyNN",
    author="Daniel",
    author_email="daniel@gmail.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifier=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        ],
    install_requires = ["matplotlib ~= 3.3.2",
                        "pytest>=3.7",
                        "tabulate >=0.8.7"
                        ],
    )
