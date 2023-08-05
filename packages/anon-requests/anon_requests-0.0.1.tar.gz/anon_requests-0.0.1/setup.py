from setuptools import setup

setup(
    name='anon_requests',
    version='0.0.1',
    packages=['anon_requests', 'anon_requests.proxy_sources'],
    url='https://github.com/OpenJarbas/anon_requests',
    install_requires=["PySocks>=1.5.7",
                      "requests>=2.11.0",
                      "stem>=1.4.0",
                      "bs4",
                      "requests_cache"],
    license='apache-2.0',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    description='anonymous requests'
)
