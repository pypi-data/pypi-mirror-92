from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4


class HideMyName(ProxyGetter):
    url = 'https://hidemy.name/en/proxy-list'

    def __init__(self, params=None, *args, **kwargs):
        self.params = params or {}
        super(HideMyName, self).__init__(*args, **kwargs)

    def scrap_proxy_list(self):
        proxies = []
        # TODO pagination, params: start += 64
        page = self.session.get(self.url,
                                headers=self.headers,
                                params=self.params)
        doc = bs4.BeautifulSoup(page.content, features="html.parser")
        for el in doc.find_all("tr"):
            fields = [e.text for e in el.find_all("td")]
            if not len(fields) or len(fields) < 7 or \
                    not fields[0][0].isdigit():
                # filter ip address rows
                continue

            ip, port, location, speed, proxy_type, anon, ts = fields
            country_code = str(el).split("class=\"flag-icon flag-icon-")[
                -1].split("\"></i>")[0].upper()
            proxy_type = proxy_type.replace(" proxy", "").lower()
            proxy_urls = {
                "http": ip + ":" + port,
                "https": ip + ":" + port
            }

            if "socks5" in proxy_type:
                proxy_type = ProxyType.SOCKS5
                proxy_urls["http"] = "socks5://" + ip + ":" + port
                proxy_urls["https"] = "socks5://" + ip + ":" + port
            elif "socks4" in proxy_type:
                proxy_type = ProxyType.SOCKS5
                proxy_urls["http"] = "socks4://" + ip + ":" + port
                proxy_urls["https"] = "socks4://" + ip + ":" + port
            elif "https" in proxy_type:
                proxy_type = ProxyType.HTTPS
            else:
                proxy_type = ProxyType.HTTP

            if anon.lower() == "high":
                anon = ProxyAnonymity.ELITE
            elif anon.lower() == "average":
                anon = ProxyAnonymity.DISTORTING
            elif anon.lower() == "low":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT

            proxies.append({"ip": ip,
                            "port": port,
                            "country_code": country_code,
                            "country_name": location.strip(),
                            "proxy_type": proxy_type,
                            "speed": speed,
                            "proxy_anonymity": anon,
                            "urls": proxy_urls,
                            "last_checked": ts})
        return proxies


# Convenience filtering
class HideMyNameHTTP(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"type": "h"}, *args, **kwargs)


class HideMyNameHTTPS(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"type": "s"}, *args, **kwargs)


class HideMyNameSOCKS4(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"type": "4"}, *args, **kwargs)


class HideMyNameSOCKS5(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"type": "5"}, *args, **kwargs)


class HideMyNameElite(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "4"}, *args, **kwargs)


class HideMyNameDistorting(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "3"}, *args, **kwargs)


class HideMyNameAnonymous(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "2"}, *args, **kwargs)


class HideMyNameTransparent(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "1"}, *args, **kwargs)


class HideMyNameEliteHTTP(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "4", "type": "h"}, *args, **kwargs)


class HideMyNameAnonymousHTTP(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "2", "type": "h"}, *args, **kwargs)


class HideMyNameDistortingHTTP(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "3", "type": "h"}, *args, **kwargs)


class HideMyNameTransparentHTTP(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "1", "type": "h"}, *args, **kwargs)


class HideMyNameEliteHTTPS(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "4", "type": "s"}, *args, **kwargs)


class HideMyNameAnonymousHTTPS(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "2", "type": "s"}, *args, **kwargs)


class HideMyNameDistortingHTTPS(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "3", "type": "s"}, *args, **kwargs)


class HideMyNameTransparentHTTPS(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "1", "type": "s"}, *args, **kwargs)


class HideMyNameEliteSOCKS5(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "4", "type": "5"}, *args, **kwargs)


class HideMyNameAnonymousSOCKS5(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "2", "type": "5"}, *args, **kwargs)


class HideMyNameDistortingSOCKS5(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "3", "type": "5"}, *args, **kwargs)


class HideMyNameTransparentSOCKS5(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "1", "type": "5"}, *args, **kwargs)


class HideMyNameEliteSOCKS4(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "4", "type": "4"}, *args, **kwargs)


class HideMyNameAnonymousSOCKS4(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "2", "type": "4"}, *args, **kwargs)


class HideMyNameDistortingSOCKS4(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "3", "type": "4"}, *args, **kwargs)


class HideMyNameTransparentSOCKS4(HideMyName):
    def __init__(self, *args, **kwargs):
        super().__init__({"anon": "1", "type": "4"}, *args, **kwargs)
