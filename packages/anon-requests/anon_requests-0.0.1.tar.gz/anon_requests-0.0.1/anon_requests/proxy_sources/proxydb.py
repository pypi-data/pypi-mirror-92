from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import requests
import bs4


class ProxyDB(ProxyGetter):
    url = 'http://proxydb.net'

    def __init__(self, scrap_countries=False,
                 transparent=True, anon=True, distorting=True, elite=True,
                 protocols=None, *args, **kwargs):
        self.scrap_countries = scrap_countries
        self.levels = []
        if transparent:
            self.levels.append(1)
        if anon:
            self.levels.append(2)
        if distorting:
            self.levels.append(3)
        if elite:
            self.levels.append(4)
        if protocols is False:
            self.protocols = []  # no filter
        else:
            self.protocols = protocols or ["http", "https", "socks4", "socks5"]
        super().__init__(*args, **kwargs)

    def _scrap_proxy_list(self, params):
        countries = [None, 'BD', 'IQ', 'HK', 'US', 'GB', 'PK', 'PL', 'SG',
                     'ID', 'RS', 'IT', 'LT', 'RU', 'DE', 'FR', 'CA', 'LY',
                     'UA', 'HU', 'CN', 'IN', 'AR', 'MX', 'TH', 'BR', 'MN',
                     'TR', 'PT']
        if self.scrap_countries is False:
            countries = [None]
        elif isinstance(self.scrap_countries, list):
            countries = self.scrap_countries
        for c in countries:
            params["country"] = c
            page = requests.get(self.url, headers=self.headers, params=params)
            doc = bs4.BeautifulSoup(page.content, features="html.parser")
            for el in doc.find_all("tr"):
                fields = [e.text for e in el.find_all("td")]
                if not len(fields):
                    continue
                fields = [f.strip() for f in fields]
                ip, port = fields[0].split(":")
                host = fields[1]
                country_code = fields[2]
                isp = fields[3]
                protocol = fields[4].lower()
                anon = fields[5].lower()
                uptime = fields[6]
                ping = fields[7]
                ts = fields[-1]
                proxy_urls = {
                    "http": ip + ":" + port,
                    "https": ip + ":" + port
                }
                proxy_type = ProxyType.HTTPS
                if protocol == "http":
                    proxy_type = ProxyType.HTTP
                elif protocol == "socks4":
                    proxy_type = ProxyType.SOCKS4
                    proxy_urls = {
                        "http": "socks4://" + ip + ":" + port,
                        "https": "socks4://" + ip + ":" + port
                    }
                elif protocol == "socks5":
                    proxy_type = ProxyType.SOCKS5
                    proxy_urls = {
                        "http": "socks5://" + ip + ":" + port,
                        "https": "socks5://" + ip + ":" + port
                    }

                if anon == "elite":
                    anon = ProxyAnonymity.ELITE
                elif anon == "anonymous":
                    anon = ProxyAnonymity.ANONYMOUS
                elif anon == "distorting":
                    anon = ProxyAnonymity.DISTORTING
                else:
                    anon = ProxyAnonymity.TRANSPARENT
                yield {"ip": ip,
                       "port": port,
                       "country_code": country_code,
                       "isp": isp,
                       "uptime": uptime,
                       "ping": ping,
                       "host": host,
                       "proxy_anonymity": anon,
                       "proxy_type": proxy_type,
                       "urls": proxy_urls,
                       "last_checked": ts}

    def scrap_proxy_list(self):
        proxies = []
        # 15 per page, trying these combinations will give more results
        # trying country code combinations will give even more results,
        # but its very slow
        for i in self.levels:
            for proto in self.protocols:
                params = {"anonlvl": i, "protocol": proto}
                for p in self._scrap_proxy_list(params):
                    if p not in proxies:
                        proxies.append(p)

            if not self.protocols:
                params = {"anonlvl": i}
                for p in self._scrap_proxy_list(params):
                    if p not in proxies:
                        proxies.append(p)

        if not self.levels:
            for proto in self.protocols:
                params = {"protocol": proto}
                for p in self._scrap_proxy_list(params):
                    if p not in proxies:
                        proxies.append(p)

        return proxies


# convenience
class ProxyDBHTTP(ProxyDB):
    def __init__(self, scrap_countries=False, transparent=True, anon=True,
                 distorting=True, elite=True, *args, **kwargs):
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, ["http"], *args, **kwargs)


class ProxyDBHTTPS(ProxyDB):
    def __init__(self, scrap_countries=False, transparent=True, anon=True,
                 distorting=True, elite=True, *args, **kwargs):
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, ["https"], *args, **kwargs)


class ProxyDBSOCKS4(ProxyDB):
    def __init__(self, scrap_countries=False, transparent=True, anon=True,
                 distorting=True, elite=True, *args, **kwargs):
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, ["socks4"], *args, **kwargs)


class ProxyDBSOCKS5(ProxyDB):
    def __init__(self, scrap_countries=False, transparent=True, anon=True,
                 distorting=True, elite=True, *args, **kwargs):
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, ["socks5"], *args, **kwargs)


class ProxyDBTransparent(ProxyDB):
    def __init__(self, scrap_countries=False, protocols=None, *args, **kwargs):
        transparent = True
        anon = False
        distorting = False
        elite = False
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, protocols, *args, **kwargs)


class ProxyDBAnonymous(ProxyDB):
    def __init__(self, scrap_countries=False, protocols=None, *args, **kwargs):
        transparent = False
        anon = True
        distorting = False
        elite = False
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, protocols, *args, **kwargs)


class ProxyDBDistorting(ProxyDB):
    def __init__(self, scrap_countries=False, protocols=None, *args, **kwargs):
        transparent = False
        anon = False
        distorting = True
        elite = False
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, protocols, *args, **kwargs)


class ProxyDBElite(ProxyDB):
    def __init__(self, scrap_countries=False, protocols=None, *args, **kwargs):
        transparent = False
        anon = False
        distorting = False
        elite = True
        super().__init__(scrap_countries, transparent, anon, distorting,
                         elite, protocols, *args, **kwargs)


class ProxyDBTransparentHTTP(ProxyDBTransparent):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["http"], *args, **kwargs)


class ProxyDBTransparentHTTPS(ProxyDBTransparent):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["https"], *args, **kwargs)


class ProxyDBTransparentSOCKS4(ProxyDBTransparent):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks4"], *args, **kwargs)


class ProxyDBTransparentSOCKS5(ProxyDBTransparent):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks5"], *args, **kwargs)


class ProxyDBAnonymousHTTP(ProxyDBAnonymous):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["http"], *args, **kwargs)


class ProxyDBAnonymousHTTPS(ProxyDBAnonymous):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["https"], *args, **kwargs)


class ProxyDBAnonymousSOCKS4(ProxyDBAnonymous):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks4"], *args, **kwargs)


class ProxyDBAnonymousSOCKS5(ProxyDBAnonymous):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks5"], *args, **kwargs)


class ProxyDBDistortingHTTP(ProxyDBDistorting):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["http"], *args, **kwargs)


class ProxyDBDistortingHTTPS(ProxyDBDistorting):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["https"], *args, **kwargs)


class ProxyDBDistortingSOCKS4(ProxyDBDistorting):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks4"], *args, **kwargs)


class ProxyDBDistortingSOCKS5(ProxyDBDistorting):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks5"], *args, **kwargs)


class ProxyDBEliteHTTP(ProxyDBElite):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["http"], *args, **kwargs)


class ProxyDBEliteHTTPS(ProxyDBElite):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["https"], *args, **kwargs)


class ProxyDBEliteSOCKS4(ProxyDBElite):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks4"], *args, **kwargs)


class ProxyDBEliteSOCKS5(ProxyDBElite):
    def __init__(self, scrap_countries=False, *args, **kwargs):
        super().__init__(scrap_countries, ["socks5"], *args, **kwargs)
