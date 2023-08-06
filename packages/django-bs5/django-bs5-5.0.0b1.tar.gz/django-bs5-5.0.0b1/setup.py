from setuptools import find_packages, setup


setup(
    name='django-bs5',
    description='simple bootstrap5 support for django',
    long_description=open('README.rst').read(),
    version='5.0.0b1',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
