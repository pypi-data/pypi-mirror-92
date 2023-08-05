import requests


class BaseSession:
    def __init__(self):
        self.refresh_session()

    def close(self):
        pass

    def refresh_session(self):
        self.session = requests.Session()
        self.rotate_identity()

    def rotate_identity(self):
        pass

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.session.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


