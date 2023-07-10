import os


class Config(object):
    # MYSQL_HOST = "172.17.122.101"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "root"
    MYSQL_PWD = "123456"
    MYSQL_PORT = 3306
    DBNAME = "rocket"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_KEY = "rocket"
    TOKEN_EXPIRATION = 336

    EXECUTOR_THREAD_POOL = 2


class FilePath(object):
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))  # ROOT_PATH

    APP_PATH = os.path.join(ROOT_PATH, "app")  # app 路径

    LOG_FILE_PATH = os.path.join(ROOT_PATH, "logs")  # 日志文件路径
    if not os.path.isdir(LOG_FILE_PATH):
        os.mkdir(LOG_FILE_PATH)

    FILE_PATH = os.path.join(ROOT_PATH, "files")  # 文件路径
    if not os.path.isdir(FILE_PATH):
        os.mkdir(FILE_PATH)

    ROCKET_SERVER = os.path.join(LOG_FILE_PATH, "rocket_server.log")

    # ROCKET_HTTP = os.path.join(LOG_FILE_PATH, "rocket_http.log")

    ROCKET_ERROR = os.path.join(LOG_FILE_PATH, "rocket_error.log")


# 项目日志滚动配置（日志文件超过10 MB就自动新建文件扩充）
LOGGING_ROTATION = "10 MB"
# 项目日志配置
LOGGING_CONF = {
    "server_handler": {
        "file": FilePath.ROCKET_SERVER,
        "level": "INFO",
        "rotation": LOGGING_ROTATION,
        "enqueue": True,
        "backtrace": False,
        "diagnose": False,
    },
    "error_handler": {
        "file": FilePath.ROCKET_ERROR,
        "level": "ERROR",
        "rotation": LOGGING_ROTATION,
        "enqueue": True,
        "backtrace": True,
        "diagnose": True,
    }
}

ROCKET_ENV = os.environ.get("rocket_env", "dev")

BANNER = """
______  _____  _____  _   __ _____  _____ 
| ___ \|  _  |/  __ \| | / /|  ___||_   _|
| |_/ /| | | || /  \/| |/ / | |__    | |  
|    / | | | || |    |    \ |  __|   | |  
| |\ \ \ \_/ /| \__/\| |\  \| |___   | |  
\_| \_| \___/  \____/\_| \_/\____/   \_/  
"""
