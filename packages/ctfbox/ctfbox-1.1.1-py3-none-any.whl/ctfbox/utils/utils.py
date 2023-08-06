from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
from binascii import hexlify, unhexlify
from hashlib import md5 as _md5
from hashlib import sha1 as _sha1
from hashlib import sha256 as _sha256
from json import dumps, loads
from random import choice, randint
from string import ascii_lowercase, digits
from urllib.parse import quote_plus, unquote_plus
from struct import pack, unpack
from typing import Union
import jwt

DEFAULT_ALPHABET = list(ascii_lowercase + digits)


def url_encode(s: str, encoding: str = 'utf-8') -> str:
    try:
        return quote_plus(s, encoding=encoding)
    except Exception:
        return ""


def url_decode(s: str, encoding: str = 'utf-8') -> str:
    try:
        return unquote_plus(s, encoding=encoding)
    except Exception:
        return ""


def base64_decode(s: str, encoding='utf-8') -> str:
    try:
        return b64decode(s.encode()).decode(encoding=encoding)
    except Exception:
        return ""


def base64_encode(s: str, encoding='utf-8') -> str:
    try:
        return b64encode(s.encode()).decode(encoding=encoding)
    except Exception:
        return ""


def bin2hex(s: str) -> str:
    try:
        return hexlify(s.encode()).decode()
    except Exception:
        return ""


def hex2bin(s: str) -> str:
    try:
        return unhexlify(s).decode()
    except Exception:
        return ""


def sha1(s: str, encoding='utf-8') -> str:
    try:
        return _sha1(s.encode(encoding=encoding)).hexdigest()
    except Exception:
        return ""


def sha256(s: str, encoding='utf-8') -> str:
    try:
        return _sha256(s.encode(encoding=encoding)).hexdigest()
    except Exception:
        return ""


def md5(s: str, encoding='utf-8') -> str:
    try:
        return _md5(s.encode(encoding=encoding)).hexdigest()
    except Exception:
        return ""


def random_int(minN: int = 0, maxN: int = 1024) -> int:
    try:
        return randint(minN, maxN)
    except Exception:
        return 0


def random_string(n: int = 32, alphabet: str = DEFAULT_ALPHABET) -> str:
    try:
        return ''.join([choice(alphabet) for _ in range(n)])
    except Exception:
        return ""


def json_encode(obj) -> object:
    try:
        return dumps(obj)
    except Exception:
        return object()


def json_decode(data) -> str:
    try:
        return loads(data)
    except Exception:
        return ""


def jwt_encode(header: dict, payload: dict, key=None, algorithm=None) -> str:
    if key is None and algorithm is None:
        # dict to json
        hearder_json = dumps(header, sort_keys=True, separators=(',', ':'))
        payload_json = dumps(payload, sort_keys=True, separators=(',', ':'))
        # json to base64
        header_b64 = urlsafe_b64encode(
            hearder_json.encode()).replace(b'=', b'')
        payload_b64 = urlsafe_b64encode(
            payload_json.encode()).replace(b'=', b'')

        return (header_b64 + b'.' + payload_b64).decode()
    else:
        return jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=header)


def jwt_decode(token: str) -> bytes:
    data = [b''] * 3
    try:
        for i, each in enumerate(token.split('.')):
            padding = 4 - len(each) % 4
            if padding:
                each += ('=' * padding)
            data[i] = urlsafe_b64decode(each.encode())
    except Exception:
        pass

    return b'-'.join(data)


def printHex(data: Union[bytes, str], up: bool = True, sep: str = ' '):
    if isinstance(data, str):
        data = data.encode()
    bs = list(data)
    for i in range(len(bs)):
        print(('%02X' if up else '%02x') % bs[i], end=sep)
        if (i+1) % 16 == 0:
            print()


def _get_pack_fmtstr(sign, endianness, N):
    byte_order = {
        'little': '<',
        'big': '>'
    }
    number_type = {
        'unsigned': {
            16: 'H',
            32: 'I',
            64: 'Q',
        },
        'signed': {
            16: 'h',
            32: 'i',
            64: 'q',
        }
    }
    return byte_order[endianness] + number_type[sign][N]


def _pN(N: int, number: int, sign: str, endianness: str) -> bytes:
    fmt = _get_pack_fmtstr(sign, endianness, N)
    # use 0xff...ff and N to calculate a mask
    return pack(fmt, number & (0xffffffffffffffff >> (64 - N)))


def p16(number: int, sign: str = 'unsigned', endianness: str = 'little') -> bytes:
    return _pN(16, number, sign, endianness)


def p32(number: int, sign: str = 'unsigned', endianness: str = 'little') -> bytes:
    return _pN(32, number, sign, endianness)


def p64(number: int, sign: str = 'unsigned', endianness: str = 'little') -> bytes:
    return _pN(64, number, sign, endianness)


def _uN(N: int, data: bytes, sign: str, endianness: str, ignore_size: bool) -> int:
    fmt = _get_pack_fmtstr(sign, endianness, N)

    if ignore_size:
        size = N // 8
        data_len = len(data)
        if data_len < size:
            data += b'\x00' * (size - data_len)
        elif data_len > size:
            data = data[:size]

    return unpack(fmt, data)[0]

def u16(data: bytes, sign: str = 'unsigned', endianness: str='little', ignore_size=True) -> int:
    return _uN(16, data, sign, endianness, ignore_size)

def u32(data: bytes, sign: str = 'unsigned', endianness: str='little', ignore_size=True) -> int:
    return _uN(32, data, sign, endianness, ignore_size)

def u64(data: bytes, sign: str = 'unsigned', endianness: str='little', ignore_size=True) -> int:
    return _uN(64, data, sign, endianness, ignore_size)
