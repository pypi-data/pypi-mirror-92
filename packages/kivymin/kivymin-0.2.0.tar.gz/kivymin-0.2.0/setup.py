from setuptools import setup

setup(
    name='kivymin',
    version='0.2.0',    
    description='Kivy Webmin Gui',
    url='https://gitlab.com/onix-os/applications/kivy-webmin',
    author='Oytun OZDEMIR',
    author_email='info@oytun.org',
    license='BSD 2-clause',
    packages=['kivymin'],
    install_requires=['kivy',
                      'cefpython3',           
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
