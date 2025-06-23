from setuptools import setup

setup(
    name='orchard-client',
    version='0.1.0',
    description='Python client for interacting with the Orchard orchestration API',
    author='Mor Dabastany',
    author_email='morpci@gmail.com',
    py_modules=['orchard_client'],
    install_requires=[
        'requests',
        'PyYAML',
    ],
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
