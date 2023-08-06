import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()
  
setuptools.setup(
  name='classofvector2d',
  version='1.0.0',
  author='Mehmet R. Irmak',
  author_email="mehmet.r.river@gmail.com",
  description='Prepared to help graphics coding for Python',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://mehmetriver.com",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows :: Windows 10",
  ],
  python_requires='>=3.6',
)

