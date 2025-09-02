from setuptools import setup, find_packages

setup(
    name="termtris",
    version="0.2.1",  # bump this for future updates
    packages=find_packages(),
    install_requires=[],  # list dependencies if any
    entry_points={
        "console_scripts": [
            "termtris=termtris.__main__:main",  # main() function in __main__.py
        ]
    },
    author="shayan",
    author_email="tomohmmdali@gmail.com",
    description="A terminal Tetris game",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shay-ff/termtris",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
