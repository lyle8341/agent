from dotenv import dotenv_values


def all_config() -> dict:
    return dotenv_values()


class Config:
    pass
