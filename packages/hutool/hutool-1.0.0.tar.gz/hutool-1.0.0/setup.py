from setuptools import setup, find_packages

setup(
    name='hutool',                          # 应用名
    version='1.0.0',                        # 版本号
    packages=find_packages('src'),          # 项目内需要被打包的所有 package
    description='Hutool for Python',
    long_description="Hutool is a small and comprehensive library of Python tools that reduce the cost of learning APIs and improve productivity through function and class encapsulation",
    package_dir={'': 'src'},                # 告诉setuptools工具包的所在的目录
    url='https://istackvip.com',
    author='isaiah',
    author_email='isaiah@sohu.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='sample tool library',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    install_requires=['PyMySQL'],
    python_requires='>=3',
    package_data={
        '': ['data/*.*'],
        '': ['*.txt', '*.yaml', '*.yml', '*.properties'],
    },
    exclude=[
        "*.test",  "*.test.*", "test.*", "test"
    ],

)
