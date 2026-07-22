from setuptools import setup, find_packages

setup(
    name="ai-media-upscaler",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-media=ai_media_upscaler.cli:main",
        ],
    },
)
