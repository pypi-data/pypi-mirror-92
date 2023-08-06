from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README



setup(
    name="predictnow-client",
    version="0.0.4",
    description="A restful client library, designed to access predictnow restful api.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Radu Ciobanu",
    author_email="radu@predictnow.ai",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(include=['predictnow' ]),
    include_package_data=True,
    install_requires=["Flask==1.1.2","gunicorn==20.0.4",
        "pandas==1.1.3",
        "honeycomb-beeline==2.13.1",
        "libhoney==1.10.0",
        "lightgbm==2.3.0",
        "pyfcm==1.4.7",
        "ray==1.0.0",
        "shap==0.33.0",
        "PyJWT==1.7.1",
        "flask-login==0.5.0",
        "flask-mail==0.9.1",
        "matplotlib==3.3.2",
        "email_validator==1.1.2",
        "paypalrestsdk==1.13.1",
        "xlrd==1.2.0",
        "redis==3.4.1",
        "future==0.18.2",
        "Flask-Bootstrap4==4.0.2",
        "firebase_admin==4.4.0",
        "wtforms==2.3.3",
        "numpy==1.19.2",
        "joblib==0.17.0",
        "werkzeug==1.0.1",
        "statsmodels==0.12.0",
        "tqdm==4.50.2",
        "scikit-learn==0.23.2",
        "requests==2.24.0",
        "setuptools==50.3.0",
        "jinja2==2.11.2",
       "stripe==2.55.1",
        "jsons==1.3.0",
        "pyarrow==2.0.0",
        "openpyxl==3.0.5"],
    python_requires='>=3.7',
    #entry_points={
    #    "console_scripts": [
    #        "weather-reporter=weather_reporter.cli:main",
    #    ]
    #},
    
)
