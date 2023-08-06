import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConstrainedKmeansCluster",  # Replace with your own username
    version="0.0.4",
    author="Sean Kaat",
    author_email="seankaat@gmail.com",
    description="A useable kmeans constrained clustering library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeanKaat/kmeansclustering",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
