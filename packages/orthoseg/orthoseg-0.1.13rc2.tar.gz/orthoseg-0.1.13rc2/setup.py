import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.1.13rc2"
with open('package_tag_version.txt', mode='w') as file:
    file.write(version)

setuptools.setup(
    name="orthoseg", 
    version=version,
    author="Pieter Roggemans",
    author_email="pieter.roggemans@gmail.com",
    description="Package to make it easier to segment orthophotos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theroggy/orthoseg",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
            "geopandas>=0.8,<0.9", "geofileops==0.1.2rc3", #"geofileops>=0.1.2,<0.2", 
            "owslib", "pycron", 
            "pillow", "rasterio", "segmentation-models>=1.0,<1.1", 
            "tensorflow>=2.4,<2.5"],
    entry_points='''
            [console_scripts]
            orthoseg=orthoseg.orthoseg:main
            ''',
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)