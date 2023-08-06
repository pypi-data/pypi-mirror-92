from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    "Operating System :: OS Independent",

]


setup(
    name="sortx",
    version="0.0.1",
    author="James Ssekitoleko",
    author_email="ssekitolekoj95@gmail.com",
    description="A small example package",
    long_description=open("README.txt").read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    python_requires='>=3.6',
)

# setup(
#     name="sortx",
#     version="0.0.1",
#     author="James Ssekitoleko",
#     author_email="ssekitolekoj95@gmail.com",
#     description="A small example package",
#     long_description=open("README.txt").read() + '\n\n' +
#     open('CHANGELOG.txt').read(),
#     long_description_content_type="text/markdown",
#     url="",
#     packages=find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
