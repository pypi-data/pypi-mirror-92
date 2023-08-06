import setuptools
with open(r'D:\Python\Pypi-uploader\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='PyEasyDownloader',
	version='1.1.5',
	author='Super_Zombi',
	author_email='super.zombi.yt@gmail.com',
	description='Track the file download process.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/PyEasyDownloader',
	packages=['PyEasyDownloader'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)