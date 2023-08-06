from setuptools import setup, find_packages

setup(name="msg_server",
      version="0.0.2",
      description="messenger_server",
      author="Yanis Kachinskis",
      author_email="yanis-k2000@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
