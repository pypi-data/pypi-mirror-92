from setuptools import setup, find_packages

# load readme
with open("README.md", 'r') as f:
    long_description = f.read()

setup(name="prettydraw",
      version="0.0.0",
      author="Chenchao Zhao",
      author_email="chenchao.zhao@gmail.com",
      url="https://github.com/ChenchaoZhao/prettydraw",
      description="Draw pretty annotations using PIL.",
      py_modules=["prettydraw"],
      package_dir={'': "prettydraw"},
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=["pillow", "numpy"],
      license="MIT")
