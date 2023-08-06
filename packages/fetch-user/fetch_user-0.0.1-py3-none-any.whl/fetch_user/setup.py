import setuptools


with open("fetch_user/README.md","r",encoding="utf-8") as fhandle:
  long_description=fhandle.read()

setuptools.setup(
    name="fetch_user", #Package Name!
    version="0.0.1", # The version of your package!
    author="pkguploaders", # Your name here!
    author_email="example@example.com", # Your e-mail here!
    description="Python Disord API wrapper for fetching users by ID", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    requirement=["requests>=2.25.1"],
    url="https://github.com", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
)
