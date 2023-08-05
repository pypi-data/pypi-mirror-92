import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygauth',
    version='1.0.0',
    install_requires=install_requires,
    author='Squili',
    description='A Python helper library for Google Authentication',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.squi.live/squili/pygauth',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5'
)
