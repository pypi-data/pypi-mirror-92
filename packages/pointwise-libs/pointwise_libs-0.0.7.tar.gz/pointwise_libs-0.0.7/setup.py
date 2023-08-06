import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pointwise_libs",
    version="0.0.7",
    author="Lieu Zheng Hong",
    author_email="lieuzhenghong@gmail.com",
    description="Helper functions for my political science research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lieuzhenghong/pointwise-libs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['docopt', 'requests', 'geopandas', 'numpy', 'pandas', 'scipy'],
    python_requires='>=3.6',
)
