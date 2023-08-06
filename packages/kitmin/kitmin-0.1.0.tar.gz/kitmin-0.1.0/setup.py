from setuptools import setup

setup(
    name='kitmin',
    version='0.1.0',    
    description='Webkit Webmin Gui',
    url='https://gitlab.com/onix-os/applications/webkit-webmin',
    author='Oytun OZDEMIR',
    author_email='info@oytun.org',
    license='BSD 2-clause',
    packages=['kitmin'],
    install_requires=['pywebview',   
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
