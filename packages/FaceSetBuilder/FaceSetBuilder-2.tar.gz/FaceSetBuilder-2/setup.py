from setuptools import setup


setup(
  name = 'FaceSetBuilder',
  packages = ['FaceSetBuilder'],
  include_package_data=True,
  version = '2',
  license='MIT',
  description = 'App to cluster faces from a dataset directory.',
  author = 'Massimo Cosimo',
  author_email = 'massimo.cosimo.95@gmail.com',
  url = 'https://github.com/max-dotpy/FaceSetBuilder',
  download_url = 'https://github.com/max-dotpy/FaceSetBuilder/archive/v0.1.tar.gz',
  keywords = ['tkinter', 'GUI', 'Face Recognition', 'Face Clustering', 'beginners-friendly', 'Dataset'],
  install_requires=[
          'Pillow',
          'opencv-python',
          'numpy',
          'imutils',
          'scikit-learn',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points={
        'console_scripts': [
            'FaceSetBuilder= FaceSetBuilder.main:start',
        ],
  },
)
