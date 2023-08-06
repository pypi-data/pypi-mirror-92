"""DB PostgreSQL関連ユティリティモジュール
内部ではpsycopg2モジュールを使用している。

Examples:
    python3 -m pypostgres 
    で引数に何もしないでスクリプトで実行するとDB設定iniファイルの雛形を出力。
    そのDB設定iniファイルはこのライブラリのconf/postgres.iniファイルである。
"""

from typing import Optional, Union, Any
from typing import Callable, NoReturn
from typing import Sequence, Iterable, List, Tuple
from typing import Dict
from typing import TypeVar, Generic, NewType, Type

import psycopg2
import configparser
import sys
import logging
import re
from libpyka.db import SQLException
from psycopg2.extensions import connection


#ロガー
logger: logging.Logger = logging.getLogger('postgres')


def get_connection(host: str='localhost', port: int=5432, user: str=None, password: str=None,
        dbname: str="db1") -> connection:
    """DBに接続し、接続オブジェクトを返す。
    DBはPostgreSQLでコネクターはpsycopg2を使用している。
    返値はpsycopg2のconnectionオブジェクトである。

    Args:
        host (str):       ホスト名
        port (int):       ポート番号
        user (str):       ユーザー名
        password (str):   パスワード
        dbname (str):     DB名
    Returns:
        psycopg2.extras.connection: DB接続オブジェクト
    Raises:
        psycopg2.Error: DB接続エラー
    """
    connect_str = "host={host} port={port} user={user} password={password} dbname={dbname}"
    connect_str = connect_str.format(host=host, port=port, 
                        user=user, password=password, dbname=dbname)
    dbcon = None
    try:
        mess = re.sub('password=(.*?) ', 'password=******', connect_str)
        logger.info('PostgreSQL接続情報 ' + mess)
        dbcon = psycopg2.connect(connect_str)
    except psycopg2.Error as ex:
        logger.error(f'DB接続時にエラー: {mess}')
        raise SQLException(f'DB接続時にエラー 接続文字列: {mess}', ex)
    return dbcon


##
# @return DBコネクションオブジェクト
# @exception psycopg2.Error   DB接続エラー
def get_config_connection(inifile: str, section: str='PostgreSQL') -> connection:
    """ini設定ファイルを読み込みそのパラメーターを元にDBに接続し、コネクションオブジェクトを返す。
    iniファイルの形式
    [postgres]  #セクション名は引数で指定可能
        host=ホスト名
        port=ポート番号
        user=ユーザー名
        password=パスワード
        dbname=DB名
    ユーザー名パスワードは必ず設定する必要がある。
    DBはPostgreSQLでコネクターはpsycopg2を使用している。

    Args:
        inifile (str): ini設定ファイル
        section (str): セクション名
    Returns:
        psycopg2.extras.connection: DB接続オブジェクト
    Raises:
        psycopg2.Error: DB接続エラー
    """
    logger.debug(f'DB接続iniファイル inifile={inifile}, section={section}')
    config = configparser.ConfigParser()
    config.read(inifile)
    params = {}
    if config.has_option(section, 'host'):
        params['host'] = config.get(section, 'host')
    if config.has_option(section, 'port'):
        params['port'] = config.get(section, 'port')
    if config.has_option(section, 'dbname'):
        params['dbname'] = config.get(section, 'dbname')
    params['user'] = config.get(section, 'user')
    params['password'] = config.get(section, 'password')
    dbcon = get_connection(**params)
    return dbcon

# *importでimportするクラス・関数
__all__ = ['get_connection', 'get_config_connection']

import os

# get_config_connection()に渡す設定iniファイルの雛形のファイル名
conf_file = '../conf/postgres.ini'

def main():
    if not os.path.exists(conf_file):
        raise Exception(f"pypostgresパッケージのiniファイルの雛形{conf_file}が存在しません。")
    with open(conf_file, 'r') as fp:
        text = fp.read()
    print(text)

if __name__ == '__main__':
    main()
