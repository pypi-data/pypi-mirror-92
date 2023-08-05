import setuptools

setuptools.setup(
    name="huyufirst",
    version="1.0.0",
    author="Yu Hu",
    author_email="huyu999999@gmail.com",
    #description="A statistical tool to quantify isoform-specific expression using long-read RNA-seq",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/WGLab/LIQA",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #install_requires=["pysam", "lifelines"],
    #python_requires='>=3.6',
    packages=["src"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "huyufirst=src.hello:main",
        ]
    },
)
