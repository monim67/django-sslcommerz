import setuptools


def get_long_description():
    with open("README.md") as file:
        return file.read()


setuptools.setup(
    name="django-sslcommerz",
    version="1.0.0",
    description="Sslcommerz for django.",
    long_description=get_long_description(),
    url="https://github.com/monim67/django-sslcommerz",
    author="Munim Munna",
    author_email="monim67@yahoo.com",
    license="MIT",
    keywords="sslcommerz",
    packages=["django_sslcommerz", "django_sslcommerz.migrations"],
    install_requires=["django>=2.0", "sslcommerz-sdk>=1.0.1"],
    python_requires=">=3",
    package_data={"django_sslcommerz": ["templates/*.html"]},
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 3.0",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
)
