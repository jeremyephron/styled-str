import setuptools

setuptools.setup(
    name="styled-str",
    version="0.0.2",
    url="https://github.com/jeremyephron/styled-str",
    author="Jeremy Ephron",
    author_email="jeremyephron@gmail.com",
    description="Colored text output in Python using ANSI escape sequences.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS'
    )
)
