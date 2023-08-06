from datetime import datetime
from distutils.core import setup
from os import path
#version = 'dev' + datetime.now().strftime(r"%Y%m%d%H%M%S")
version = '0.0.1-alpha1'
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='django-file-transfer-automator',
    packages=['file_transfer_automator'],
    version=version,
    license='lgpl-3.0',
    description='File Transfer Automation Library',
       long_description=long_description,
    long_description_content_type='text/markdown',
    author='Swaroop P',
    author_email='iamswaroopp@gmail.com',
    url='https://gitlab.com/iamswaroopp/django-file-transfer-automator',
    download_url='https://gitlab.com/iamswaroopp/django-file-transfer-automator/-/archive/' + version +
    '/django-file-transfer-automator-' + version + '.zip',
    keywords=['django', 'celery', 'file', 'file transfer', 'automation', 'scheduler'],
    install_requires=[
        'django',
        'celery',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
