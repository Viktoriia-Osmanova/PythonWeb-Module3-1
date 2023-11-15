from setuptools import setup, find_packages

setup(name = 'clean_folder',
      version = '0.0.1',
      packages = find_packages(),
      author = 'Go_IT',
      description = "clean folder from trash",
      entry_points = {
          'console_scripts' : ['clean-folder = clean_folder.clean:main']
      },
      install_requires = [
          'numpy',
          'Pillow',
          ],
)