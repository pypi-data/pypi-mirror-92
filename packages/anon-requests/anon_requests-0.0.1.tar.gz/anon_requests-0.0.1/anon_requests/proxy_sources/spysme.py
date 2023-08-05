from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType


class SpysMe(ProxyGetter):
    url = 'https://spys.me/proxy.txt'

    def scrap_proxy_list(self):
        proxies = []
        page = self.session.get(self.url, headers=self.headers)
        data = [p.strip() for p in page.text.split("\n") if p and p[
            0].isdigit()]
        for p in data:
            p = p.replace("!", "")
            proxy, fields = p.split(" ")[:2]
            ip, port = proxy.split(":")
            if fields.endswith("-S"):
                proxy_type = ProxyType.HTTPS
                fields = fields[:-2]
            else:
                proxy_type = ProxyType.HTTP

            country_code, anon = fields.split("-")
            if anon == "H":
                anon = ProxyAnonymity.ELITE
            elif anon == "A":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT
            proxies.append({"ip": ip,
                            "port": port,
                            "country_code": country_code,
                            "proxy_anonymity": anon,
                            "proxy_type": proxy_type,
                            "urls": {"http": proxy,
                                     "https": proxy}
                            })
        return proxies


class SpysMeGithub(SpysMe):
    url = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'


# convenience
class SpysMeHTTPSGithub(SpysMeGithub):
    url = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'

    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if p["proxy_type"] == ProxyType.HTTPS]


class SpysMeHTTPS(SpysMe):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if p["proxy_type"] == ProxyType.HTTPS]


class SpysMeAnonymous(SpysMe):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class SpysMeElite(SpysMe):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]


class SpysMeHTTPSAnonymous(SpysMeHTTPS):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class SpysMeHTTPSElite(SpysMeHTTPS):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]
