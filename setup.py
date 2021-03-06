import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pubmedy",  # Replace with your own username
    version="0.0.1",
    author="Théophraste HENRY",
    author_email="theophraste.henry@gmail.com",
    description="A lightweight Biopython-based interface to NCBI's Entrez API, created to speed up systematic literature reviews",
    long_description=long_description,
    long_description_content_type="text/markdown",
    licence="Apache License 2.0",
    url="https://github.com/lescientifik/pubmedy",
    packages=setuptools.find_packages(),
    install_requires=["biopython"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["pubmedy = pubmedy.main:cli"]},
)
