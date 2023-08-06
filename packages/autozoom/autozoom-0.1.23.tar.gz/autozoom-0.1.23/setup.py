from setuptools import setup
from setuptools import find_packages
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(name="autozoom",
      version="0.1.23",
      description="Based on a schedule enter zoom meetings",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/DogAteMyCode/autozoom',
      author="VoidNull",
      author_email="nullvoid0div0@protonmail.com",
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          "pyperclip",
          "keyboard>0.13.0",
          "requests",
          "texttable"
      ],
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: MacOS"],
      python_requires='>=3.6',
      include_package_data=False
      )
