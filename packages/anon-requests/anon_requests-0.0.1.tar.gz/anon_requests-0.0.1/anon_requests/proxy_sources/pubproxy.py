from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import requests


class PubProxy(ProxyGetter):
    # http://pubproxy.com get an api key
    url = 'http://pubproxy.com/api/proxy'

    def __init__(self, params=None, key=None, *args, **kwargs):
        self.params = params or {"limit": 5}
        self.params["format"] = "json"
        if key:
            self.params["api"] = key
        super(PubProxy, self).__init__(*args, **kwargs)

    def scrap_proxy_list(self):
        proxies = []
        data = requests.get(self.url, params=self.params)
        for p in data.json()["data"]:
            support = p["support"]
            proxy_type = ProxyType.HTTP
            anon = ProxyAnonymity.TRANSPARENT
            proxy_urls = {
                "http": p["ipPort"],
                "https": p["ipPort"]
            }
            if support["https"]:
                proxy_type = ProxyType.HTTPS
            if p["proxy_level"] == "elite":
                anon = ProxyAnonymity.ELITE
            elif p["proxy_level"] == "anonymous":
                anon = ProxyAnonymity.ANONYMOUS

            if p["type"] == "socks5":
                anon = ProxyType.SOCKS5
                proxy_urls = {
                    "http": "socks5://" + p["ipPort"],
                    "https": "socks5://" + p["ipPort"]
                }
            if p["type"] == "socks4":
                anon = ProxyType.SOCKS4
                proxy_urls = {
                    "http": "socks4://" + p["ipPort"],
                    "https": "socks4://" + p["ipPort"]
                }

            proxies.append({"ip": p["ip"],
                            "port": p["port"],
                            "country_code": p["country"],
                            "proxy_anonymity": anon,
                            "google": bool(support["google"]),
                            "proxy_type": proxy_type,
                            "urls": proxy_urls,
                            "speed": p["speed"],
                            "last_checked": p["last_checked"]})
        return proxies


# convenience imports
class PubProxyHTTP(PubProxy):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["type"] = "http"


class PubProxyHTTPAnonymous(PubProxyHTTP):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxyHTTPElite(PubProxyHTTP):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"


class PubProxyHTTPS(PubProxyHTTP):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["https"] = True


class PubProxyHTTPSAnonymous(PubProxyHTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxyHTTPSElite(PubProxyHTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"


class PubProxySOCKS4(PubProxy):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["type"] = "socks4"


class PubProxySOCKS5(PubProxy):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["type"] = "socks5"


class PubProxySOCKS4Anonymous(PubProxySOCKS4):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxySOCKS5Anonymous(PubProxySOCKS5):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxySOCKS4Elite(PubProxySOCKS4):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"


class PubProxySOCKS5Elite(PubProxySOCKS5):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"


class PubProxySOCKS4HTTPS(PubProxySOCKS4):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["https"] = True


class PubProxySOCKS5HTTPS(PubProxySOCKS5):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["https"] = True


class PubProxySOCKS4HTTPSAnonymous(PubProxySOCKS4HTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxySOCKS5HTTPSAnonymous(PubProxySOCKS5HTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "anonymous"


class PubProxySOCKS4HTTPSElite(PubProxySOCKS4HTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"


class PubProxySOCKS5HTTPSElite(PubProxySOCKS5HTTPS):
    def __init__(self, params=None, key=None, *args, **kwargs):
        super().__init__(params, key, *args, **kwargs)
        self.params["level"] = "elite"
