from kwonfig.constants import DHALL_SUPPORTED
from . import Handler

if DHALL_SUPPORTED:
    import dhall


class DhallHandler(Handler):
    enabled = DHALL_SUPPORTED

    suffix = 'dhall'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        return dhall.load(fp)
