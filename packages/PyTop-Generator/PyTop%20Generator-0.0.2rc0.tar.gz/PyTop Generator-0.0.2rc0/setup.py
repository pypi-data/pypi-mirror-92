from setuptools import setup, find_packages

setup(
    name="PyTop Generator",
    version="0.0.2pre",
    description="A package to generate desktop files for your python script.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Fabian Becker",
    author_email="fab.becker@protonmail.com",
    url="https://gitlab.com/Raspilot/pytop-generator",
    download_url="https://gitlab.com/Raspilot/pytop-generator.git",
    packages=[x for x in find_packages() if not x.startswith("test")],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
    ],
    license="BSD License",
    keywords="desktop files icon shortcut pytop generator",
    entry_points={
        "console_scripts": [
            "add_this_to_desktop=desktop_file_generator.generator:automatic"
        ],
    },
)
