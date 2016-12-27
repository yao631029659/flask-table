#这个是配置文件目录 等下main要调用里面的部分信息
class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

# class DevConfig(object):  刚开始可以用这句 但是到了表单验证的时候就要改过来了
class DevConfig(Config):
    #写了这句等下有提示
    DEBUG = True
    # 这个是sqlalchemy的uri
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    # 写了这句可以看到sql语句
    SQLALCHEMY_ECHO=True
