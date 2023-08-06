from setuptools import find_namespace_packages, setup


setup(
    name='societeinfo',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Python wrapper to SOCIETE INFO api.',
    long_description='Python wrapper to SOCIETE INFO api. See https://gitlab.com/PierreKephas/societeinfo-python.',
    author='Pierre Kephas',
    url='https://gitlab.com/PierreKephas/societeinfo-python',
    packages=find_namespace_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=[
    ],
    install_requires=[
        'requests>=2,<3',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-import-order',
            'pytest',
            'pytest-cov',
            'pytest-xdist',
            'requests-mock',
        ],
    },
)
