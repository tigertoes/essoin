import time
from email.utils import parseaddr
from essoin.types import AddrType, NetType, BandwidthType, EncryptionMethod, MediaType


class SessionDescription():

    def __init__(self):
        self.media = []
        self.time = []

    def add(self, key, value):
        # TODO This interface may change in the future to handle multiple
        setattr(self, key, value)


class Essoin():

    """ Seconds delta between NTP and UNIX epochs """
    NTP_UNIX_OFFSET = 2208988800

    def __init__(self):
        self.types = {
            'v': self._parse_version,
            'o': self._parse_origin,
            's': self._parse_session_name,
            'i': self._parse_session_description,
            'u': self._parse_uri,
            'e': self._parse_email,
            'p': self._parse_phone,
            'c': self._parse_connection_data,
            'b': self._parse_bandwidth,
            't': self._parse_time,
            'r': self._parse_repeat,
            'z': self._parse_tz,
            'k': self._parse_key,
            'm': self._parse_media,
            'a': self._parse_attribute
        }

    def parse(self, payload):
        if not isinstance(payload, str):
            raise ValueError('Payload MUST be a str')
        sd = SessionDescription()
        is_media = 0
        media = False
        attributes = []
        for line in payload.splitlines():
            if len(line) < 3 or not line[:1].islower() or line[1] != '=':
                raise SdpParseException('Invalid Session Description')
            sdp_type = line[:1]
            content = line[2:]
            processor = self.types.get(sdp_type)
            if not processor:
                raise SdpParseException('Invalid type "{}"'.format(sdp_type))
            (key_name, value) = processor(content)

            # FSM states:
            # 0 - Not yet come across a media description
            # 1 - Media Description
            if is_media == 0:
                if key_name == 'media':
                    media = value
                    is_media = 1
                else:
                    sd.add(key_name, value)
            elif is_media == 1:
                if key_name == 'attribute':
                    attributes.append(value)
                else:
                    sd.media.append({
                        'media': media,
                        'attributes': attributes
                    })
                    attributes = []
                    is_media = 0

        # Clean out any values once out of the loop
        if is_media > 0:
            sd.media.append({
                'media': media,
                'attributes': attributes
            })
        return sd

    def _parse_version(self, payload):
        payload = int(payload)
        if payload != 0:
            raise SdpParseException('Unsupported version')
        return ('version', payload)

    def _parse_origin(self, payload):
        try:
            (user, sess_id, sess_version, nettype, addrtype, addr) = payload.split(' ')
        except ValueError:
            raise SdpParseException('Missing number of elements in origin')
        nettype = NetType[nettype]
        addrtype = AddrType[addrtype]
        return ('origin', {
            'user': user,
            'session_id': sess_id,
            'session_version': sess_version,
            'nettype': nettype,
            'addrtype': addrtype,
            'address': addr
        })

    def _parse_session_name(self, payload):
        return ('name', str(payload))

    def _parse_session_description(self, payload):
        return ('description', str(payload))

    def _parse_uri(self, payload):
        # TODO this should be validated with a URI parsing library
        return ('uri', str(payload))

    def _parse_email(self, payload):
        # TODO Consider a better way of handling this as it's basic.
        #      As pointed out on SO (https://stackoverflow.com/a/14485817), the
        #      email.utils parser lets plenty of edge cases in.
        if parseaddr(payload) == ('', ''):
            raise SdpParseException('Email appears invalid')
        return ('email', str(payload))

    def _parse_phone(self, payload):
        return ('phone', str(payload))

    def _parse_connection_data(self, payload):
        try:
            (nettype, addrtype, address) = payload.split(' ')
        except ValueError:
            raise SdpParseException('Incorrect number of elements in connection')
        nettype = NetType[nettype]
        addrtype = AddrType[addrtype]
        return ('connection', {
            'nettype': nettype,
            'addrtype': addrtype,
            'address': str(address)
        })

    def _parse_bandwidth(self, payload):
        try:
            (bw_type, bandwidth) = payload.split(':')
        except ValueError:
            raise SdpParseException('Incorrect arguments in bandwidth')
        # FIXME Handle "X-" types
        bw_type = BandwidthType[bw_type]
        return ('bandwidth', {
            'type': bw_type,
            'bandwidth': str(bandwidth)
        })

    def _parse_time(self, payload):
        try:
            (start, end) = payload.split(' ')
        except ValueError:
            raise SdpParseException('Invalid time range')
        return ('time', {
            'start': time.gmtime(int(start) - Essoin.NTP_UNIX_OFFSET),
            'end': time.gmtime(int(end) - Essoin.NTP_UNIX_OFFSET)
        })

    def _parse_repeat(self, payload):
        fields = payload.split(' ')
        for field in fields:
            field = self._convert_time(field)
        return ('repeat', {
           'interval': fields[0],
           'active_duration': fields[1],
           'start_offsets': fields[2:]
        })

    def _parse_tz(self, payload):
        fields = payload.split(' ')
        timezones = []
        if len(fields) % 2:
            raise SdpParseException('Uneven number of times and offsets')
        fields = iter(fields)
        for field in fields:
            (adj_time, offset) = (field, next(fields))
            adj_time = time.gmtime(int(adj_time) - Essoin.NTP_UNIX_OFFSET)
            offset = self._convert_time(str(offset))
            timezones.append((adj_time, offset))
        return ('tz', timezones)

    def _parse_key(self, payload):
        fields = payload.split(':')
        key = False
        if len(fields) > 2:
            raise SdpParseException('Incorrect arguments in encryption key')
        elif len(fields) == 2:
            key = fields[1]
        method = EncryptionMethod[fields[0]]
        return ('key', {
            'method': method,
            'key': key
        })

    def _parse_media(self, payload):
        (media, ports, proto, fmt) = payload.split(' ')
        media_type = MediaType[media]
        return ('media', {
            'type': media_type,
            'ports': ports,  # TODO Handle port ranges correctly
            'proto': proto,
            'fmt': fmt
        })

    def _parse_attribute(self, payload):
        name = False
        value = False
        if ":" in payload:
            try:
                (name, value) = payload.split(':')
            except ValueError:
                raise SdpParseException('Attribute appears invalid')
            value = value.split(' ')
        else:
            name = payload
        # TODO Handle each known attribute type
        return ('attribute', {
            'name': name,
            'value': value
        })

    def _convert_time(self, time):
        """ Convert short hand (e.g. "1h") into seconds """
        if time[-1].islower():
            if time[-1] == 's':
                time = int(time[:-1])
            elif time[-1] == 'm':
                time = int(time[:-1]) * 60
            elif time[-1] == 'h':
                time = int(time[:-1]) * 3600
            elif time[-1] == 'd':
                time = int(time[:-1]) * 86400
            else:
                raise SdpParseException('Unknown interval "{}"'.format(time[-1]))
        return time


class SdpParseException(Exception):
    pass
