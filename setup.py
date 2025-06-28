from setuptools import setup, find_packages

setup(
    name="ai-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.2.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "langchain>=0.0.267",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
    ],
    python_requires=">=3.9",
    author="",
    author_email="",
    description="AI Core framework",
    keywords="ai, machine learning, nlp",
    url="",
) 