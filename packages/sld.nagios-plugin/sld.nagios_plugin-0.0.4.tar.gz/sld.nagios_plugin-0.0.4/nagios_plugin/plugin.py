import sys


class ReturnCode:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        pass


def get_plugin_output(message, perf_data):
    _plugin_output = ""
    if message is not None:
        _plugin_output = message
        if perf_data is not None:
            _plugin_output = _plugin_output + f" | {perf_data}"
    return _plugin_output


class Plugin:
    def __init__(self):
        self.return_codes = ReturnCode()
        self.default_return_code = self.return_codes.UNKNOWN
        self._return_code = None

    @property
    def return_code(self):
        if self._return_code is None:
            return self.default_return_code
        else:
            return self._return_code

    @return_code.setter
    def return_code(self, value):
        self._return_code = value

    def _return(self, **kwargs):
        message = kwargs.get("message", None)
        perf_data = kwargs.get("perf_data", None)
        plugin_output = get_plugin_output(message, perf_data)
        if plugin_output is not None:
            print(plugin_output)
        raise sys.exit(self.return_code)

    def return_ok(self, **kwargs):
        self.return_code = self.return_codes.OK
        self._return(**kwargs)

    def return_warning(self, **kwargs):
        self._return_code = self.return_codes.WARNING
        self._return(**kwargs)

    def return_critical(self, **kwargs):
        self._return_code = self.return_codes.CRITICAL
        self._return(**kwargs)

    def return_unknown(self, **kwargs):
        self._return_code = self.return_codes.UNKNOWN
        self._return(**kwargs)
