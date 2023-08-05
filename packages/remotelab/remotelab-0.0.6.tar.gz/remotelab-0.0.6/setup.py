import setuptools

setuptools.setup(
	name="remotelab",
	version="0.0.6",
	author="Umut Ediz",
	author_email="umtedz@gmail.com",
	description="Simplified interaction library for Acrome Remote Lab products",
	#url="https://github.com/Acrome-Remote-Laboratory/RemoteLabHW",
	license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
	install_requires = ['crccheck', 'pyserial'],
	packages=setuptools.find_packages(),
	python_requires='>=3.6',

)
