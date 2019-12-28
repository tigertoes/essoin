from enum import Enum


class AddrType(Enum):
    IP4 = 1
    IP6 = 2
    NSAP = 3
    GWID = 4
    E164 = 5


class NetType(Enum):
    IN = 1
    TN = 2
    ATM = 3
    PSTN = 4


class BandwidthType(Enum):
    CT = 1
    AS = 2
    RS = 3
    RR = 4
    TIAS = 5


class KeyType(Enum):
    clear = 1
    base64 = 2
    uri = 3
    prompt = 4


class EncryptionMethod(Enum):
    clear = 1
    base64 = 2
    uri = 3
    prompt = 4


class MediaType(Enum):
    audio = 1
    video = 2
    text = 3
    application = 4
    message = 5
    image = 6
