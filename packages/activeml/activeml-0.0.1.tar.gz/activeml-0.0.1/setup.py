import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="activeml",
    version="0.0.1",
    author="Zakaria Chowdhury",
    author_email="info@zakariachowdhury.com",
    description="A streamlit app for visual data anlysis, processing and machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zakariachowdhury/activeml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)