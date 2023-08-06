import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'bot_config'

setuptools.setup(
    name="bot_config",
    version="0.2.18",
    author="Kristof & Zselter",
    description="bot_config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kopnt/bot_config",
    packages=setuptools.find_packages(),
    install_requires=["amazon_platform", "kcu", "selenium_uploader_account", "amazon_config", "amazon_buddy", "selenium_facebook", "selenium_instagram", "selenium_tiktok", "selenium_twitter", "selenium_youtube", "simple_multiprocessing"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)