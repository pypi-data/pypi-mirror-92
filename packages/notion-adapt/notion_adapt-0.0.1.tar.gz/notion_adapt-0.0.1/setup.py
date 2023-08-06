from setuptools import setup

setup(
   name='notion_adapt',
   version='0.0.1',
   description='notion-py with auto multiselect tage creation',
   author='uzapolsky',
   author_email='uzapolsky@gmail.com',
   packages=['notion_adapt'],  #same as name
   install_requires=['bs4', 'cached-property', 'commonmark', 'dictdiffer', 'python-slugify', 'requests', 'tzlocal'] #external packages as dependencies
)