from setuptools import setup, find_packages

setup(name="mess_server_prj_Ruslan",
      version="0.0.1",
      description="mess_server_prj",
      author="Ruslan",
      author_email="huzin.ruslan@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
