from setuptools import setup, find_packages

# requires = ["aniso8601==8.1.0", "certifi==2020.12.5", "chardet==3.0.4", "click==7.1.2"
#             "gevent==20.12.1", "greenlet==0.4.17", "idna==2.10", "itsdangerous==1.1.0",
#             "Mako==1.1.3", "MarkupSafe==1.1.1", "pika==1.1.0", "python-dateutil==2.8.1",
#             "python-editor==1.0.4", "pytz==2020.5", "requests==2.25.0", "simplejson==3.17.2",
#             "six==1.15.0", "tzlocal==2.1", "urllib3==1.26.2", "zope.event==4.5.0", "zope.interface==5.2.0"]  # 需要安装的第三方依赖

setup(
    name="shopex-dingding-notify",
    version=2.3,
    description="ShopEx dingding notify for python",
    long_description=open("README.md").read(),
    packages=find_packages(),
    author="ShopEx",
    author_email="xuhongtao@shopex.cn",
    license="LGPL",
    url="https://github.com/magic119/shopex_dingding_notify.git",
    platforms=["README.md"],
    python_requires='>=3.6',
    # install_requires=requires
)