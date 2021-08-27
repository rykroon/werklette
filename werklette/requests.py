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
        return getattr(self, '_path_params', {})

