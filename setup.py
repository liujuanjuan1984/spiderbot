import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spiderbot",
    version="0.2.0",
    author="liujuanjuan1984",
    author_email="qiaoanlu@163.com",
    description="a spider bot (scrawler) by python, using selenium and chrome driver",
    keywords=["selenium", "spider", "chrome", "bot", "scrawler"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liujuanjuan1984/spiderbot",
    project_urls={
        "Github Repo": "https://github.com/liujuanjuan1984/spiderbot",
        "Bug Tracker": "https://github.com/liujuanjuan1984/spiderbot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["example"]),
    python_requires=">=3.5",
    install_requires=["selenium"],
)
