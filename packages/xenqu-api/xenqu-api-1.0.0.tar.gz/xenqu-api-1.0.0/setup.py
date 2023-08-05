import setuptools

setuptools.setup(
    name="xenqu-api",
    version="1.0.0",
    author="Charles Buffington II",
    author_email="charles.buffington@essium.co",
    description="A full implementation of the Xenqu API in Python.",
    url="https://github.com/EssiumLLC/lib-xenqu-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)