from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Kangana',
    version='0.0.2',
    description='Python package to encrypt and decrypt files.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='moridb',
    author_email='elogger@web.de',
    license='MIT',
    classifiers=classifiers,
    keywords='kangana',
    packages=find_packages(),
    install_requires=['']
)