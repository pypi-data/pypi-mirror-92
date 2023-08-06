"""SQLのエラーを表す例外クラス。
DB関連全てのエラーを表してもいる。
"""

from typing import Optional, Union, Any
from typing import Callable, NoReturn
from typing import Sequence, Iterable, List, Tuple
from typing import Dict
from typing import TypeVar, Generic, NewType, Type

from ..utils import AbstractException

# Exceptionのサブクラスを表すGeneric型
E = NewType('E', BaseException)

class SQLException(AbstractException):
    """DB関連のエラーを表す基底クラス。
    utils.AbstractExceptionを継承してもいる。

    Args:
        mess (str): エラーメッセージ
        nextex (Exception): エラーの元になった例外
    """
    ##
    # @brief  コンストラクタ
    #
    # @param mess エラーメッセージ
    # @param nextex 例外の元になった例外
    def __init__(self, mess: str, nextex: Optional[E]=None) -> None:
        self.message = mess
        self.nextex = nextex

# *importでimportするクラス・関数
__all__ = ['SQLException']

