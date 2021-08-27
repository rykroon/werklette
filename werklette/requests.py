from werkzeug.wrappers import WerkRequest


class Request(WerkRequest):

    @property
    def query_params(self):
        """
            Alias for for request.args
        """
        return self.args