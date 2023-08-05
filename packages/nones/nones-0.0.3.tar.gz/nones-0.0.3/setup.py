import setuptools

long_description = '''
Values for using in default arguments.Example:
	def func(f=lambda:None):
		return f()
	# Tip: func(f=<function <lambda> at 0x73a8cd2a60>)
	from nones import NONE_AS_FUNC
	def func(f=NONE_AS_FUNC):
		return f()
	# Tip: func(f=func)
'''

setuptools.setup(
    name="nones", # Replace with your own username
    version="0.0.3",
    author='Vadim Simakin',
    author_email="sima.vad@gmail.com",
    description="Values for using in default arguments.",
    long_description=long_description,
    long_description_content_type="text/plain",
    py_modules=['nones'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.1'
)