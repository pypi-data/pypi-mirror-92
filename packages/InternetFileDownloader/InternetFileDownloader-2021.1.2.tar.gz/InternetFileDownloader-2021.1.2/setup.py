from setuptools import setup
setup(
    name="InternetFileDownloader",
    version="2021.1.2",
    description="This is a file downloader.",
    author="Pranav",
    packages=["FileDownloader"],
    entry_points={
    'console_scripts': [
        'InternetFileDownloader=FileDownloader.FileDownloader:main',
    ],
},
    install_requires=["requests"],

    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)