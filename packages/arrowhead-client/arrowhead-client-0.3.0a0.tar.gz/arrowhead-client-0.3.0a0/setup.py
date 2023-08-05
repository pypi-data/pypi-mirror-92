import setuptools
import _version

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name=_version.__lib_name__,
        version=_version.__version__,
        author=_version.__author__,
        author_email=_version.__email__,
        description='Arrowhead client library',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/arrowhead-f/client-library-python',
        packages=setuptools.find_packages(exclude=['tests', 'examples']),
        license='EPL-2.0',
        install_requires=[
            'Flask>=1.0.2',
            'requests>=2.21',
            'gevent>=20.5.0',
            'typing-extensions>=3.7'
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Operating System :: POSIX :: Linux',
            'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
        ],
        python_requires='>=3.7'
)
