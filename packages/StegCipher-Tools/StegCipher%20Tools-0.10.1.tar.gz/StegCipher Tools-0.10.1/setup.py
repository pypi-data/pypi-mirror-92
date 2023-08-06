from setuptools import setup
setup(
    name="StegCipher Tools",
    version="0.10.1",
    description="Collection of lib and GUI tool for steganography/manage/encrypt/decrypt your credentials.",
    #long_description=README,
    #long_description_content_type="text/markdown",
    url="https://github.com/samsepiol-e/cipher",
    author="Sam Sepiol",
    author_email="0.alicegawa@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["CipherLib"],
    include_package_data=True,
    install_requires=[
        "pybase64", "pycrypto", "pillow", 'pyperclip', 'ttkthemes'
    ],
    entry_points={"console_scripts": [
        "credtools=Cred.__main__:main",
        "stegtools=Steg.__main__:main"
        ]},
)
