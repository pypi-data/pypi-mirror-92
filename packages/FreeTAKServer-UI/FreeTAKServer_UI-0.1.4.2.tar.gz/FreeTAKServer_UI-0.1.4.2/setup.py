from setuptools import setup

setup(
    name='FreeTAKServer_UI',
    version='0.1.4.2',
    packages=['FreeTAKServer-UI', 'FreeTAKServer-UI.app', 'FreeTAKServer-UI.app.base', 'FreeTAKServer-UI.app.home', 'FreeTAKServer-UI.tests'],
    url='https://github.com/FreeTAKTeam/FreeTakServer',
    license='Eclipse License',
    author='Ghost, C0rv0',
    author_email='example@email.com',
    description='fawfwfa',
    install_requires = [
        "flask",
        "flask_login",
        "flask_migrate",
        "flask_wtf",
        "flask_sqlalchemy",
        "email_validator",
        "gunicorn",
        "python-decouple",
        "sqlalchemy-utils"
    ],
    include_package_data=True
)
