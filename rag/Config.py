from dotenv import dotenv_values


def all_config() -> dict:
    return dotenv_values() # 加载当前目录下的 .env 文件


class Config:
    pass
