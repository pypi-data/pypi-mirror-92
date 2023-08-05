from anon_requests.base_session import BaseSession
from anon_requests.proxy_sources import ProxyGetter, ProxyType, ProxyAnonymity
from anon_requests.proxy_sources.free_proxy_list import SSLProxies, \
    SocksProxy, FreeProxyList, UKProxy, USProxy, AnonProxies
from anon_requests.proxy_sources.free_proxy_cz import FreeProxyCZ
from anon_requests.proxy_sources.hidemyname import HideMyName
from anon_requests.proxy_sources.proxydb import ProxyDB
from anon_requests.proxy_sources.proxyscan import ProxyScan
from anon_requests.proxy_sources.pubproxy import PubProxy
from anon_requests.proxy_sources.spysme import SpysMe
from anon_requests.proxy_sources.spysone import SpysOne
from anon_requests.proxy_sources.proxynova import ProxyNova
from anon_requests.exceptions import NoMoreProxies
import random
import concurrent.futures


class ProxyLeech(ProxyGetter):
    def scrap_proxy_list(self):
        proxy_list = []
        if self.verbose:
            print("scrapping proxies")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) \
                as executor:
            sources = [SSLProxies(), HideMyName(), FreeProxyCZ(),
                       ProxyDB(), ProxyScan(), PubProxy(),
                       SpysMe(), FreeProxyList(), SocksProxy(), USProxy(),
                       UKProxy(), AnonProxies(), SpysOne(), ProxyNova()]
            # Start the scrap operations and mark each future with its source
            future_to_source = {
                executor.submit(s.scrap_proxy_list): s for s in sources}
            for future in concurrent.futures.as_completed(future_to_source):
                new = future.result()
                proxy_list += new
                if self.verbose:
                    print(future_to_source[future].__class__.__name__,
                          len(new), "proxies scrapped")
        return proxy_list


class ProxySession(BaseSession):
    def __init__(self, proxy_provider=None,
                 proxy_type=ProxyType.ANY,
                 proxy_anonymity=ProxyAnonymity.ANY,
                 country_codes=None, validate=False, ignore_bad=True):
        proxy_provider = proxy_provider or ProxyLeech(
            proxy_anonymity=proxy_anonymity, proxy_type=proxy_type)
        self.proxy_provider = proxy_provider
        self.proxy_type = proxy_type
        self.anonymity = proxy_anonymity
        self.country_codes = country_codes or []
        if validate:
            self.proxy_provider.validate()
        if ignore_bad:
            self.proxy_provider.remove_bad_proxies()
        super().__init__()

    @property
    def current_proxy(self):
        return self.session.proxies

    def rotate_identity(self):
        kwargs = {}
        if self.proxy_type != ProxyType.ANY:
            kwargs["proxy_type"] = self.proxy_type
        if self.anonymity != ProxyAnonymity.ANY:
            kwargs["proxy_anonymity"] = self.anonymity
        if self.country_codes:
            kwargs["country_code"] = random.choice(self.country_codes)
        proxy = self.proxy_provider.get(**kwargs)
        self.session.proxies.update(proxy["urls"])

    def set_proxy(self, proxy):
        self.session.proxies.update(proxy)


class RotatingProxySession(ProxySession):
    def rotate(self):
        try:
            self.rotate_identity()
        except NoMoreProxies:
            if len(self.proxy_provider.used_proxies) == 0:
                # TODO custom exception
                raise  # no proxies scrapped at all
            # reset used proxy list
            self.proxy_provider.used_proxies = []
        self.rotate_identity()

    def get(self, *args, **kwargs):
        # TODO add some limit
        while True:
            try:
                self.rotate()
                return self.session.get(*args, **kwargs)
            except Exception as e:
                # next proxy
                pass

    def post(self, *args, **kwargs):
        # TODO add some limit
        while True:
            try:
                self.rotate()
                return self.session.post(*args, **kwargs)
            except Exception as e:
                # next proxy
                pass

    def put(self, *args, **kwargs):
        # TODO add some limit
        while True:
            try:
                self.rotate()
                return self.session.put(*args, **kwargs)
            except Exception as e:
                # next proxy
                pass

    def patch(self, *args, **kwargs):
        # TODO add some limit
        while True:
            try:
                self.rotate()
                return self.session.patch(*args, **kwargs)
            except Exception as e:
                # next proxy
                pass

    def delete(self, *args, **kwargs):
        # TODO add some limit
        while True:
            try:
                self.rotate()
                return self.session.delete(*args, **kwargs)
            except Exception as e:
                # next proxy
                pass