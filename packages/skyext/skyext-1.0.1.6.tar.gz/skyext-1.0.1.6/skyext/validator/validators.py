from __future__ import unicode_literals

import math
import re
import uuid

try:
    import ipaddress
except ImportError:
    ipaddress = None

__all__ = (
    'Email', 'email',
    'IPAddress', 'ip_address', 'Length',
    'length', 'NumberRange', 'number_range',
    'Required', 'required', 'Regexp', 'regexp', 'URL', 'url',
    'UUID',
    'ValidationError', 'StopValidation'
)


class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


class StopValidation(Exception):
    """
    Causes the validation chain to stop.

    If StopValidation is raised, no more validators in the validation chain are
    called. If raised with a message, the message will be added to the errors
    list.
    """
    def __init__(self, message='', *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)



class Length(object):
    def __init__(self, min=-1, max=-1, message=None):
        assert min != -1 or max != -1, 'At least one of `min` or `max` must be specified.'
        assert max == -1 or min <= max, '`min` cannot be more than `max`.'
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field, field_name, field_val):
        if not isinstance(field_val, str):
            field_val = str(field_val)
        l = field_val and len(field_val) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                message = 'Field must be between %(min)d and %(max)d characters long.' % dict(min=self.min, max=self.max, length=l)

            raise ValidationError(message)


class NumberRange(object):
    def __init__(self, min=None, max=None, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field, field_name, field_val):
        data = field_val
        if data is None or math.isnan(data) or (self.min is not None and data < self.min) or \
                (self.max is not None and data > self.max):
            message = self.message
            if message is None:
                if self.max is None:
                    message = field.gettext('Number must be at least %(min)s.')
                elif self.min is None:
                    message = field.gettext('Number must be at most %(max)s.')
                else:
                    message = field.gettext('Number must be between %(min)s and %(max)s.')

                message = message % dict(min=self.min, max=self.max)

            raise ValidationError(message)


class Required(object):
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field, field_name, field_val):
        if not field_val and not str(field_val).strip():
            if self.message is None:
                message = field.gettext('This field {0} is required.' % str(field_name))
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class Regexp(object):
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, form, field, field_name, field_val, message=None):
        match = self.regex.match(field_val or '')
        if not match:
            if message is None:
                if self.message is None:
                    message = 'Invalid input.'
                else:
                    message = self.message

            raise ValidationError(message)
        return match


class Email(object):
    def __init__(self, message=None):
        self.message = message
        self.reg = ".*@.*"

    def __call__(self, form, field, field_name, field_val):
        match = self.reg.match(field_val or '')
        if not match:
            if self.message is None:
                message = 'Invalid email input.'
            else:
                message = self.message

            raise ValidationError(message)
        return match


class IPAddress(object):
    """
    Validates an IP address. Requires ipaddress package to be instaled for Python 2 support.

    :param ipv4:
        If True, accept IPv4 addresses as valid (default True)
    :param ipv6:
        If True, accept IPv6 addresses as valid (default False)
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, ipv4=True, ipv6=False, message=None):
        if ipaddress is None:
            raise Exception("Install 'ipaddress' for Python 2 support.")
        if not ipv4 and not ipv6:
            raise ValueError('IP Address Validator must have at least one of ipv4 or ipv6 enabled.')
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.message = message

    def __call__(self, form, field, field_name, field_val):
        value = field_val
        valid = False
        if value:
            valid = (self.ipv4 and self.check_ipv4(value)) or (self.ipv6 and self.check_ipv6(value))

        if not valid:
            message = self.message
            if message is None:
                message = field.gettext('Invalid IP address.')
            raise ValidationError(message)

    @classmethod
    def check_ipv4(cls, value):
        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            return False

        if not isinstance(address, ipaddress.IPv4Address):
            return False

        return True

    @classmethod
    def check_ipv6(cls, value):
        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            return False

        if not isinstance(address, ipaddress.IPv6Address):
            return False

        return True


class URL(Regexp):
    def __init__(self, require_tld=True, message=None):
        regex = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        super(URL, self).__init__(regex, re.IGNORECASE, message)
        self.validate_hostname = HostnameValidation(
            require_tld=require_tld,
            allow_ip=True,
        )

    def __call__(self, form, field, field_name, field_val):
        message = self.message
        if message is None:
            message = field.gettext('Invalid URL.')

        match = super(URL, self).__call__(form, field, field_val, message)
        if not self.validate_hostname(match.group('host')):
            raise ValidationError(message)


class UUID(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field, field_name, field_val):
        message = self.message
        if message is None:
            message = field.gettext('Invalid UUID.')
        try:
            uuid.UUID(field_val)
        except ValueError:
            raise ValidationError(message)


class HostnameValidation(object):
    hostname_part = re.compile(r'^(xn-|[a-z0-9_]+)(-[a-z0-9_]+)*$', re.IGNORECASE)
    tld_part = re.compile(r'^([a-z]{2,20}|xn--([a-z0-9]+-)*[a-z0-9]+)$', re.IGNORECASE)

    def __init__(self, require_tld=True, allow_ip=False):
        self.require_tld = require_tld
        self.allow_ip = allow_ip

    def __call__(self, hostname):
        if self.allow_ip:
            if IPAddress.check_ipv4(hostname) or IPAddress.check_ipv6(hostname):
                return True

        # Encode out IDNA hostnames. This makes further validation easier.
        try:
            hostname = hostname.encode('idna')
        except UnicodeError:
            pass

        # Turn back into a string in Python 3x
        if not isinstance(hostname, str):
            hostname = hostname.decode('ascii')

        if len(hostname) > 253:
            return False

        # Check that all labels in the hostname are valid
        parts = hostname.split('.')
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not self.hostname_part.match(part):
                return False

        if self.require_tld:
            if len(parts) < 2 or not self.tld_part.match(parts[-1]):
                return False

        return True


email = Email
ip_address = IPAddress
length = Length
number_range = NumberRange
required = Required
regexp = Regexp
url = URL