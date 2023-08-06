class SanetinelException(Exception):
    pass


class UnknownChannelException(SanetinelException):
    def __init__(self, sanetinel_name: str, channel_name: str):
        super(UnknownChannelException, self).__init__()
        self._sanetinel_name: str = sanetinel_name
        self._channel_name: str = channel_name

    def __repr__(self):
        return f"Sanetinel {self._sanetinel_name} does not have a channel called " \
               f"'{self._channel_name}' but a log was made to it at test time!"

    def __str__(self):
        return repr(self)
