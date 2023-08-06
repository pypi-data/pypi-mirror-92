from setuptools import setup, find_packages

setup(name="msg_client_gb",
      version="0.0.2",
      description="messenger_client",
      author="Yanis Kachinskis",
      author_email="yanis-k2000@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
