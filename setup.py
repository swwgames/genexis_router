from setuptools import setup, find_packages

setup(
    name="genexis_router",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "macaddress",
        "ipaddress",
    ],
    entry_points={
        "console_scripts": [
            "genexis_router=genexis_router.router:main",
        ],
    },
    author="swwgames",
    author_email="your.email@example.com",
    description="A library to interact with Genexis routers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/swwgames/genexis_router",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)