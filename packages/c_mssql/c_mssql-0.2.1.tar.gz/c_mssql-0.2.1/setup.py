from setuptools import setup, find_packages  

# with open("tencent_message\README.md", "r",encoding="utf-8") as fh:
#     long_description = fh.read()
long_description="1-use pyodbc instead of pymssql.\n2-add trust connection"
setup(  
    name = 'c_mssql',  
    version = '0.2.1',
    # keywords = ('chinesename',),  
    description = 'c_mssql',  
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT tencent_message',  
    install_requires = ["pyodbc","c_sql"],  
    packages = ['c_mssql'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'evanyang',  
    author_email = 'lightyiyi@qq.com',
    url = 'https://www.cnblogs.com/Evan-fanfan/',
    # packages = find_packages(include=("*"),),  
)  


# python setup.py check #检查写的有没有问题，有问题就直接报错了
# python setup.py sdist upload #压缩、并打包上传到pip源上，会在当前目录下产生一个dist文件夹
# #里面就是打好的压缩包
 
# python setup.py sdist #只压缩不上传，就是打成tar.gz这种安装包，给别人用的话直接给他安装包就可以了