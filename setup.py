from setuptools import setup, find_packages

setup(
    name="trading-simulator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "yfinance>=0.2.36",
        "plotly>=5.18.0",
    ],
    python_requires=">=3.8",
) 