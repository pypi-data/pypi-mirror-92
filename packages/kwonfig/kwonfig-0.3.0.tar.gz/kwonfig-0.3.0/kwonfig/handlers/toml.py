from kwonfig.constants import TOML_SUPPORTED
from . import Handler

if TOML_SUPPORTED:
    try:
        import rtoml as toml
    except ImportError:
        import qtoml as toml


class TomlHandler(Handler):
    enabled = TOML_SUPPORTED

    suffix = 'toml'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        return toml.load(fp)
