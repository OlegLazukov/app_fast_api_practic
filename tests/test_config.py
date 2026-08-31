import os

from dotenv import load_dotenv

config_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(config_dir, '.test.env')
load_dotenv(dotenv_path)


class TestSettings:
    MODE: str = os.environ.get('MODE_TEST')

    DB_HOST: str = os.environ.get('DB_TEST_HOST')
    DB_PORT: int = os.environ.get('DB_TEST_PORT')
    DB_USER: str = os.environ.get('DB_TEST_USER')
    DB_PASS: str = os.environ.get('DB_TEST_PASS')
    DB_NAME: str = os.environ.get('DB_TEST_NAME')


    DB_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

test_settings = TestSettings()