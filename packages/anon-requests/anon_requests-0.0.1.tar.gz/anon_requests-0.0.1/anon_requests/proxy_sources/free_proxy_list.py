from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4


class FreeProxyList(ProxyGetter):
    url = 'https://free-proxy-list.net'

    def scrap_proxy_list(self):
        proxies = []
        page = self.session.get(self.url, headers=self.headers)
        doc = bs4.BeautifulSoup(page.content, features="html.parser")
        for el in doc.find_all("tr"):
            fields = [e.text for e in el.find_all("td")]
            if not len(fields) or len(fields) < 8 or \
                    not fields[0][0].isdigit():
                # filter ip address rows
                continue
            ip = fields[0]
            port = fields[1]
            proxy_urls = {
                "http":  ip + ":" + port,
                "https":  ip + ":" + port
            }
            proxy_type = ProxyType.HTTP
            if fields[6] == "yes":
                proxy_type = ProxyType.HTTPS

            anon = fields[4].replace(" proxy", "").lower()
            if anon == "elite":
                anon = ProxyAnonymity.ELITE
            elif anon == "anonymous":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT
            proxies.append({"ip": ip,
                            "port": port,
                            "country_code": fields[2],
                            "country_name": fields[3],
                            "proxy_anonymity": anon,
                            "google": fields[5],
                            "proxy_type": proxy_type,
                            "urls": proxy_urls,
                            "last_checked": fields[7]})
        return proxies


class SocksProxy(FreeProxyList):
    url = 'https://www.socks-proxy.net'

    def scrap_proxy_list(self):
        proxies = []
        page = self.session.get(self.url)
        doc = bs4.BeautifulSoup(page.content, features="html.parser")
        for el in doc.find_all("tr"):
            fields = [e.text for e in el.find_all("td")]
            if not len(fields) or len(fields) < 8 or \
                    not fields[0][0].isdigit():
                # filter ip address rows
                continue
            proxy_urls = {}
            proxy_type = ProxyType.SOCKS4
            if fields[4].lower() == "socks4":
                proxy_urls["https"] = "socks4://" + fields[0] + ":" + fields[1]
                proxy_urls["http"] = "socks4://" + fields[0] + ":" + fields[1]
            if fields[4].lower() == "socks5":
                proxy_type = ProxyType.SOCKS5
                proxy_urls["http"] = "socks5://" + fields[0] + ":" + fields[1]
                proxy_urls["https"] = "socks5://" + fields[0] + ":" + fields[1]

            anon = fields[5].replace(" proxy", "").lower()
            if anon == "elite":
                anon = ProxyAnonymity.ELITE
            elif anon == "anonymous":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT

            proxies.append({"ip": fields[0],
                            "port": fields[1],
                            "country_code": fields[2],
                            "country_name": fields[3],
                            "proxy_type": proxy_type,
                            "proxy_anonymity": anon,
                            "urls": proxy_urls,
                            "last_checked": fields[7]})
        return proxies


class SSLProxies(FreeProxyList):
    url = 'https://www.sslproxies.org'


class UKProxy(FreeProxyList):
    url = 'https://free-proxy-list.net/uk-proxy.html'


class USProxy(FreeProxyList):
    url = 'https://www.us-proxy.org/'


class AnonProxies(FreeProxyList):
    url = 'https://free-proxy-list.net/anonymous-proxy.html'
