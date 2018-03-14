from setuptools import setup

setup(name='weeb.py',
      author='Desiiii',
      author_email='godavaru@gmail.com',
      description='An API wrapper for weeb.sh',
      url='https://github.com/Desiiii/weeb.py',
      version='1.0.4',
      packages=["weeb"],
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
      ],
      python_requires=">=3.4, <4",
      include_package_date=True)