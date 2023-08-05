import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(name="labext",
      version='4.1.6',
      packages=find_packages(),
      description="Extra widgets for Jupyter Lab",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Binh Vu",
      author_email="binh@toan2.com",
      url="https://github.com/binh-vu/labext",
      python_requires='>3.6',
      license="MIT",
      install_requires=['ipywidgets', 'IPython', 'jupyter_core', 'requests', 'ipyevents', 'ipycallback>=0.2.5', 'ujson'],
      package_data={'': ['*.js', '*.ts']})
