"""libpykaライブラリのdbパッケージのpypostgresモジュールのテスト
"""

from typing import Optional, Union, Any
from typing import Callable, NoReturn
from typing import Sequence, Iterable, List, Tuple
from typing import Dict
from typing import TypeVar, Generic, NewType, Type

import logging
import unittest
from libpyka.db import pypostgres
from libpyka.db import SQLException

"""モジュールpypostgresのテストケースクラス。
"""
class PyPostgresTest(unittest.TestCase):
    CONNECT_INFO_OK = {
        "host": "mail.kacpp.xyz",
        "port": 5432,
        "user": "postkamail",
        "password": "postkamail3275",
        "dbname": "kamail"
    }
    CONNECT_INFO_ERR = {
        "host": "mail.kacpp.xyz",
        "port": 5432,
        "user": "kamail",
        "password": "kamailadmin",
        "dbname": "kamail"
    }

    """このテストケース前に呼ばれる関数。
    """
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)

    def test_get_connection(self) -> None:
        """DB接続ができるかテストする。
        """
        dbcon = pypostgres.get_connection(**PyPostgresTest.CONNECT_INFO_OK)
        self.assertTrue(dbcon is not None)

    def test_get_connection_connect_error(self) -> None:
        """誤りのDB接続情報でちゃんとエラーが出るかテストする。
        """
        with self.assertRaises(SQLException):
            dbcon = pypostgres.get_connection(**PyPostgresTest.CONNECT_INFO_ERR)
    
    def test_get_config_connection(self) -> None:
        """設定iniファイルから接続情報を読み込みDBに接続できるかテスト。
        """
        inifile = 'tests/data/postgres.ini'
        section = 'PostgreSQL'
        dbcon = pypostgres.get_config_connection(inifile, section)
        self.assertTrue(dbcon is not None)


