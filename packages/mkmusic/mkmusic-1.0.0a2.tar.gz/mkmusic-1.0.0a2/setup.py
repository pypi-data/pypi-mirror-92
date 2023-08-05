import setuptools
import mkmusic.version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkmusic",
    version=mkmusic.version.ver,
    author="Hyperhydrochloric Acid",
    author_email="HCl_10@outlook.com",
    description="Make your music with short code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HCl-10/mkmusic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'mkmusic = mkmusic:start_program'
        ]
    },
    python_requires='>=3.0',
    install_requires=[
        'numpy',
        'tqdm'
    ]
)
