import logging
import cicd.secret

def get_secret_strings():
    secret_dict = cicd.secret.__dict__
    props = [item for item in secret_dict.keys() if not item.startswith("__") and item.isupper()]
    return list(map(lambda prop: secret_dict[prop], props))

strings_to_mask = get_secret_strings()

# https://relaxdiego.com/2014/07/logging-in-python.html
class SensitiveDataFilter(logging.Filter):
    
    def __init__(self, patterns):
        super(SensitiveDataFilter, self).__init__()
        self._patterns = patterns

    def filter_exc_info(self, exc_info):
        for info in exc_info:
            if isinstance(info, Exception):
                if isinstance(info.args, dict):
                    for k in info.args.keys():
                        info.args[k] = self.redact(info.args[k])
                else:
                    info.args = tuple(self.redact(arg) for arg in info.args)

                # This is a bit of a hack to prevent CalledProcessError from
                # showing secrets used in subprocess executed commands.
                # A more generic way to handle this would be awesome.
                if 'cmd' in info.__dict__.keys():
                    if isinstance(info.cmd, dict):
                        for k in info.cmd.keys():
                            info.cmd[k] = self.redact(info.cmd[k])
                    elif isinstance(info.cmd, list):
                        info.cmd = tuple(self.redact(cmd) for cmd in info.cmd)
                    elif isinstance(info.cmd, str):
                        info.cmd = self.redact(cmd)

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if record.exc_info:
            self.filter_exc_info(record.exc_info)
        return True

    def redact(self, msg):
        msg = str(msg) #isinstance(msg, basestring) and msg or str(msg)
        for pattern in self._patterns:
               msg = msg.replace(pattern, '************', 10)
        return msg


stream_handler = logging.StreamHandler()
stream_handler.addFilter(SensitiveDataFilter(strings_to_mask))
logging.basicConfig(
    level=logging.WARNING,
    handlers=[
        stream_handler,
    ],
)

for handler in logging.root.handlers:
    handler.addFilter(SensitiveDataFilter(strings_to_mask))

log = logging.getLogger(__name__)

