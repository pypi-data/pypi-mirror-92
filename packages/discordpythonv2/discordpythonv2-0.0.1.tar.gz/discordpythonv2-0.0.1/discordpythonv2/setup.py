import setuptools
setuptools.setup(
    name="discordpythonv2", 
    version="0.0.1", 
    author="Caipie123", 
    author_email="example@example.com", 
    description="Discord.py cog", 
    long_description="Cog",
    long_description_content_type="text/markdown",install_requires=["discord.py>=1.6.0"],
    url="https://github.com/", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)