#这个是配置文件目录 等下main要调用里面的部分信息
class DevConfig(object):
    #写了这句等下有提示
    DEBUG = True
    # 这个是sqlalchemy的uri
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    # 写了这句可以看到sql语句
    SQLALCHEMY_ECHO=True
