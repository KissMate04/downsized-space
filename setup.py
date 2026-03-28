from setuptools import setup, find_packages

setup(
    name="downsized-space",
    version="0.1.0",
    packages=find_packages(include=["downsized_space", "downsized_space.*"]),
    package_data={
        "downsized-space": ["sprites/*.png"],
    },
    include_package_data=True,
    install_requires=[
        "pygame~=2.6.1",
        "setuptools~=80.3.1",
    ],
    entry_points={
        "console_scripts": [
            "downsized-space=downsized_space.launcher:main",
        ],
    },
    author="Kiss Máté",
    author_email="matekiss424@gmail.com",
    url="https://github.com/KissMate04/downsized-space",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
