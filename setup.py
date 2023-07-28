from setuptools import setup

readme = ""
with open("README.md", "r") as fh:
    readme = fh.read()
    # search for any lines that contain <img and remove them
    readme = readme.split("\n")
    readme = [line for line in readme if "<img" not in line]
    # now join all the lines back together
    readme = "\n".join(readme)


setup(
    name="agentloop",
    version="0.1.5",
    description="A simple, lightweight loop for your agent.",
    long_description=readme,  # added this line
    long_description_content_type="text/markdown",  # and this line
    url="https://github.com/AutonomousResearchGroup/agentloop",
    author="Moon",
    author_email="shawmakesmagic@gmail.com",
    license="MIT",
    packages=["agentloop"],
    install_requires=["pynput"],
    readme="README.md",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
