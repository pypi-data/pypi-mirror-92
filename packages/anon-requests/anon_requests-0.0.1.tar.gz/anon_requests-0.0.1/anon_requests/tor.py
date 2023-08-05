import stem
from stem.control import Controller
from stem.process import launch_tor_with_config
import time
import requests
from anon_requests.base_session import BaseSession


class TorSession(BaseSession):
    def __init__(self,
                 proxy_port=9050,
                 ctrl_port=9051,
                 password=None):

        self.proxy_port = proxy_port
        self.ctrl_port = ctrl_port

        self._tor_proc = None
        if not self._tor_process_exists():
            self._tor_proc = self._launch_tor()

        self.ctrl = Controller.from_port(port=self.ctrl_port)
        self.ctrl.authenticate(password=password)

        super(TorSession, self).__init__()

    def refresh_session(self):
        self.session = requests.Session()
        self.session.proxies.update({
            'http': 'socks5://localhost:%d' % self.proxy_port,
            'https': 'socks5://localhost:%d' % self.proxy_port,
        })

    def rotate_identity(self):
        self._new_circuit_async()
        time.sleep(self.ctrl.get_newnym_wait())
        self.refresh_session()

    def _tor_process_exists(self):
        try:
            ctrl = Controller.from_port(port=self.ctrl_port)
            ctrl.close()
            return True
        except:
            return False

    def _launch_tor(self):
        return launch_tor_with_config(
            config={
                'SocksPort': str(self.proxy_port),
                'ControlPort': str(self.ctrl_port)
            },
            take_ownership=True)

    def close(self):
        try:
            self.session.close()
        except:
            pass

        try:
            self.ctrl.close()
        except:
            pass

        if self._tor_proc:
            self._tor_proc.terminate()

    def _new_circuit_async(self):
        self.ctrl.signal(stem.Signal.NEWNYM)


class RotatingTorSession(TorSession):
    def get(self, *args, **kwargs):
        self.rotate_identity()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.rotate_identity()
        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs):
        self.rotate_identity()
        return super().put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        self.rotate_identity()
        return super().patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.rotate_identity()
        return super().delete(*args, **kwargs)
