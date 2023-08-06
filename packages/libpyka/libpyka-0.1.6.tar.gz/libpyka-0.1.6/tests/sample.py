from pathlib import Path

# path = Path('tests') / __file__
# print(path)
# print(__file__)

import hashlib
import libpyka
from libpyka.utils import bytes_enc
from libpyka.utils import hashint, hashint64
from libpyka.utils import MAX_UNSIGNED_INT, MAX_UNSIGNED_LONG
import subprocess
from subprocess import Popen
from pathlib import Path

def hash_to_int(hashval: str, max_range: int=MAX_UNSIGNED_INT) -> int:
    """ハッシュ値の文字列から整数値を組み立てて返す。
    ハッシュ値は文字列を指定する。
    ハッシュ値の文字列の一個一個の文字からUnicode Pointを求めて、
    その合計でハッシュの整数値を求めている。
    Args:
        hashval (str): ハッシュ値
        max_range (int): 整数値の範囲
    Returns:
        int: 文字列のハッシュ値から生成した整数値
    """
    ret = 1
    for ch in hashval:
        val = ord(ch)
        ret = ret + val
    ret = ret * 1234567
    return ret % max_range

fname = 'data/logo.png'
path = Path('tests') / fname
cmd = f'sha256sum {path}'
proc = Popen(cmd, shell=True, stdout=subprocess.PIPE)
result = proc.stdout.read().decode('utf-8')
shhash = re.sub(r'[ \t]+.*$', '', result)
print(shhash + "test")
proc.wait()
byte_content = path.read_bytes()
sha256 = hashlib.sha256()
sha256.update(byte_content)
hashval = sha256.hexdigest()
print(hashval)
