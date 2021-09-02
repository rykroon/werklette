from werkzeug.datastructures import ImmutableDict
from werkzeug.wrappers import Request as WerkzeugRequest


class Request(WerkzeugRequest):

    @property
    def query_params(self):
        """
            Alias for for request.args
        """
        return self.args

    @property
    def path_params(self):
        return getattr(self, '_path_params', ImmutableDict())

    def _set_path_params(self, params):
        self._path_params = ImmutableDict(params)

