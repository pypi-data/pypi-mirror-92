import setuptools

with open('README.rst', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(
    name='xapy',
    version='0.0.1',
    author='Jasper Bok',
    author_email='hello@jasperbok.nl',
    description='A Python wrapper around the xapi.us Xbox API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/jasperbok/xapy',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)