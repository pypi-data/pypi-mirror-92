from setuptools import setup, find_packages

setup(name='mestpy',
      version='0.4.2',
      description='Gauss-Jordan Elimination in Teaching, Work with docs of main professional educational program',
      packages=find_packages( include=['mestpy','mestpy.*']),
      install_requires = [ 
        'pandas >= 0.23.3', 
        'NumPy >= 1.14.5', 
		'docx2pdf >=0.1.7',
		'PyPDF2>=1.26.0',
		'python-docx>=0.8.10',
		'xlrd >=2.0.1',
		'openpyxl >= 3.0.4',
		'XlsxWriter >= 1.3.7'
        ],
      extras_require = { 
        'interactive' :  ['jupyter']
		},
      author ='Mestnikov S.V.',
      author_email='mestsv@mail.ru',
      zip_safe=False)
