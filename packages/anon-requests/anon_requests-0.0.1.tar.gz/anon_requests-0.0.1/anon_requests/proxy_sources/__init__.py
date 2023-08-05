import random
import requests_cache
from enum import Enum
from anon_requests.exceptions import NoMoreProxies
from anon_requests.utils import get_headers
import concurrent.futures
import requests


class ProxyAnonymity(str, Enum):
    TRANSPARENT = "transparent"
    ANONYMOUS = "anonymous"
    DISTORTING = "distorting"
    ELITE = "elite"
    ANY = "any"


class ProxyType(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"
    ANY = "any"


class ProxyGetter:
    url = "google.com"

    def __init__(self, proxy_type=ProxyType.ANY,
                 proxy_anonymity=ProxyAnonymity.ANY, headers=None, ttl=120,
                 verbose=False, workers=20,
                 test_url='http://ipecho.net/plain', timeout=5):
        self.used_proxies = []
        self.bad_proxies = []
        self.good_proxies = []
        # cache for 2 minutes between scrapping new proxy list
        self.session = requests_cache.CachedSession(expire_after=ttl,
                                                    backend="memory")
        self.headers = headers or get_headers()
        self.headers['Referer'] = self.url
        self.verbose = verbose
        self.workers = workers
        self.test_url = test_url
        self.timeout = timeout
        self.proxy_type = proxy_type
        self.proxy_anonymity = proxy_anonymity
        self.all_proxies = self.scrap_proxy_list()

    def get(self, proxy_anonymity=ProxyAnonymity.ANY,
            proxy_type=ProxyType.ANY, country_code=None, reuse=False):

        # previous filtered list of good proxies
        good_proxies = list(self.good_proxies)

        # scrap fresh
        proxies = self.get_proxy_list()

        # filter bad proxies
        proxies = [p for p in proxies if p not in self.bad_proxies]

        # filter by proxy anonymity
        if proxy_anonymity != ProxyAnonymity.ANY:
            proxies = [p for p in proxies if
                       p["proxy_anonymity"] == proxy_anonymity]
            good_proxies = [p for p in good_proxies if
                            p["proxy_anonymity"] == proxy_anonymity]

        # filter by proxy type
        if proxy_type != ProxyType.ANY:
            proxies = [p for p in proxies if p["proxy_type"] == proxy_type]
            good_proxies = [p for p in good_proxies if
                            p["proxy_type"] == proxy_type]

        # filter by country
        if country_code:
            # TODO country name instead of code ?
            proxies = [p for p in proxies if
                       p["country_code"] == country_code]
            good_proxies = [p for p in good_proxies if
                            p["country_code"] == country_code]

        # don't get same proxy twice
        if not reuse:
            proxies = [p for p in proxies if p not in self.used_proxies]
            good_proxies = [p for p in good_proxies if
                            p not in self.used_proxies]

        if len(good_proxies):
            proxy = random.choice(good_proxies)
        else:
            if not len(proxies):
                raise NoMoreProxies
            proxy = random.choice(proxies)
        self.used_proxies.append(proxy)
        return proxy

    def scrap_proxy_list(self):
        raise NotImplementedError

    def get_proxy_list(self):
        proxies = self.all_proxies
        if self.proxy_type != ProxyType.ANY:
            proxies = [p for p in proxies if
                       p["proxy_type"] == self.proxy_type]
        if self.proxy_anonymity != ProxyAnonymity.ANY:
            proxies = [p for p in proxies if
                       p["proxy_anonymity"] == self.proxy_anonymity]
        return proxies

    def refresh_proxies(self):
        self.all_proxies = self.scrap_proxy_list()

    def validate(self):
        if self.verbose:
            print("Validating proxies")

        def do_validation(proxy):
            try:
                response = requests.get(self.test_url,
                                        proxies=proxy["urls"],
                                        timeout=self.timeout)
                if response.status_code != 200:
                    raise ConnectionError
                if self.verbose:
                    print(proxy["ip"] + ":" + proxy["port"], "OK")
                return True
            except Exception as e:
                #print("bad proxy, not working or very slow!")
                #print(session.current_proxy)
                #print(e)
                if self.verbose:
                    print(proxy["ip"] + ":" + proxy["port"], "BAD")
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) \
                as executor:
            # Start the validation operations and mark each future with its
            # proxy
            future_to_proxy = {executor.submit(do_validation, p): p for p in
                               self.get_proxy_list()}
            for future in concurrent.futures.as_completed(future_to_proxy):
                good = future.result()
                proxy = future_to_proxy[future]
                if good:
                    self.good_proxies.append(proxy)
                else:
                    self.bad_proxies.append(proxy)

    def remove_bad_proxies(self):
        for p in self.bad_proxies:
            if p in self.all_proxies:
                self.all_proxies.remove(p)

