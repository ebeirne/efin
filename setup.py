from setuptools import setup, find_packages

setup(
    name="efin",
    version="1.5.0",  # Updated version to reflect new features
    author="Ethan Beirne",
    author_email="ethan.g.beirne@gmail.com",
    description="A comprehensive financial analysis and forecasting library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ebeirne/efin",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "yfinance",           # Financial data retrieval
        "statsmodels",        # ARIMA, SARIMA, SARIMAX models
        "prophet",            # Prophet forecasting model
        "click",              # Command-line interface
        "requests_cache",     # HTTP caching for data requests
        "matplotlib",         # Plotting and visualization
        "numpy",              # Numerical operations
        "pandas",             # Data manipulation and analysis
        "scikit-learn",         
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust license if needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
