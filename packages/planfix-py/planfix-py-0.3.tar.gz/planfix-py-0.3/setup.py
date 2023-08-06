from setuptools import setup 


with open('README.md', 'r') as file:
	long_description = file.read()

setup(
	name='planfix-py',
	version='0.3',
	license='MIT',
	description='Python package for working with Planfix API',

	long_description=long_description,
    long_description_content_type='text/markdown',

	url='https://github.com/LD31D/planfix_py',

	author='LD31D',
	author_email='artem.12m21@gmail.com',

	packages=['planfix_py'],

	install_requires=[
		'requests',
		'jinja2'
    ],

	zip_safe=False
)
