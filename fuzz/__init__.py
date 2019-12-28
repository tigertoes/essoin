from essoin import Essoin, SdpParseException
from pythonfuzz.main import PythonFuzz

essoin = Essoin()

@PythonFuzz
def fuzz_runner(buf):
    try:
        string = buf.decode('utf8')
        essoin.parse(string)
    
    # KeyError: when lookup against a type does not match
    except KeyError as e:
        pass

    # ValueError: when given argument is not a string
    except ValueError as e:
        pass

    # SdpParseException: All other exceptions
    except SdpParseException:
       pass
