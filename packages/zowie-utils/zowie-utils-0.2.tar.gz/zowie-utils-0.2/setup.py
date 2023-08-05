from distutils.core import setup

setup(
    name="zowie-utils",
    packages=["zowie"],
    version="0.2",
    license="MIT",
    description="Zowie python commons",
    author="zowie-dev",
    author_email="lukasz.kazmierczak@zowie.ai",
    url="https://github.com/chatbotizeteam/python-commons",
    keywords=[],
    install_requires=[
        "regex",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
