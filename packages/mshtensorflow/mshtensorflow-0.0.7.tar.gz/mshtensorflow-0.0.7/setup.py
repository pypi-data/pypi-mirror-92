from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="mshtensorflow",
    version="0.0.7",
    description="A free and simple deep learning framework for everyone",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/adhamhesham97/Deep-Learning-framework",
    download_url = 'https://github.com/adhamhesham97/Deep-Learning-framework/archive/0.0.6.tar.gz',
    author="salah adel",
    author_email="salahadel820@gmail.com",
    keywords="framework",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        ],
    include_package_data=True,
    zip_safe=False,
)