from setuptools import setup
setup(
    name="PackageInstaller",
    version="2021.1.2",
    description="This is a Easy Package Installer.",
    author="Pranav",
    entry_points={
    'console_scripts': [
        'PackageInstaller=PackageInstaller:main',
    ],
},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)