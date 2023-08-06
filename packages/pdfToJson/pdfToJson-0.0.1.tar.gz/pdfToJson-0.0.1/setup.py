import setuptools
with open('README.md','r') as f:
    long_description = f.read()

setuptools.setup(
    name ='pdfToJson',
    version ='0.0.1',
    author ='xjw',
    author_email = 'XiongJingWen_0629@163.com',
    description = 'This is a package which converts pdf to json using GROBID',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = setuptools.find_packages()
)