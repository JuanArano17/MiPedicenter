class Config:
    SECRET_KEY = '4ecd725281820152a8d856062cbc77'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' 
    SQLALCHEMY_DATABASE_URI = 'postgres://zonmaomrqubdfk:d84eceb66361cd9ee37c9d80fe1874bc6a3201dc3328c734cae8ae5b19aba0fa@ec2-3-222-74-92.compute-1.amazonaws.com:5432/da0et3jea36bcb'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'mipedicenter@gmail.com'
    MAIL_PASSWORD = 'pediarenalescenter' 
    #MAIL_PASSWORD = 'mmfeflirnoyrdbrh'
    MAIL_USE_TSL = False
    MAIL_USE_SSL = True