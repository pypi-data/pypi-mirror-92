from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4
import base64


class FreeProxyCZ(ProxyGetter):
    url = 'http://free-proxy.cz/en/proxylist/country/all/all/ping/all'

    def scrap_proxy_list(self, page_num=1):
        proxies = []
        page = self.session.get(self.url + "/" + str(page_num),
                                headers=self.headers)
        doc = bs4.BeautifulSoup(page.content, features="html.parser")
        for el in doc.find_all("tr"):
            fields = [e.text for e in el.find_all("td")]
            if len(fields) < 10:
                continue

            ip = el.find("script")
            ip = str(ip).split("(\"")[-1].split("\")")[0]
            ip = base64.b64decode(ip.encode("utf-8")).decode("utf-8")
            port = fields[1]
            proxy_type = fields[2].lower()
            country_name = fields[3].strip()
            region = fields[4]
            city = fields[5]
            anon = fields[6]
            speed = fields[7].strip()
            uptime = fields[8]
            ts = fields[-1]
            flag = el.find("a")["href"].split("/en/proxylist/country/")[
                1].split("/")[0]

            proxy_urls = {
                "http":  ip + ":" + port,
                "https":  ip + ":" + port
            }

            if proxy_type == "https":
                proxy_type = ProxyType.HTTPS
            else:
                proxy_type = ProxyType.HTTP
            if proxy_type == "socks4":
                proxy_type = ProxyType.SOCKS4
                proxy_urls = {
                    "http": "socks4://" + ip + ":" + port,
                    "https": "socks4://" + ip + ":" + port
                }
            elif proxy_type == "socks5":
                proxy_type = ProxyType.SOCKS5
                proxy_urls = {
                    "http": "socks5://" + ip + ":" + port,
                    "https": "socks5://" + ip + ":" + port
                }

            if anon == "High anonymity":
                anon = ProxyAnonymity.ELITE
            elif anon == "Anonymous":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT
            proxies.append({"ip": ip,
                            "port": port,
                            "country_code": flag,
                            "country_name": country_name,
                            "region": region,
                            "city": city,
                            "proxy_anonymity": anon,
                            "proxy_type": proxy_type,
                            "speed": speed,
                            "uptime": uptime,
                            "urls": proxy_urls,
                            "last_checked": ts})
        # pagination
        if page_num < 5:
            try:
                proxies += self.scrap_proxy_list(page_num + 1)
            except:
                pass
        return proxies


class FreeProxyCZTransparent(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/all/ping/level3'


class FreeProxyCZElite(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/all/ping/level1'


class FreeProxyCZAnonymous(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/all/ping/level2'


class FreeProxyCZHTTP(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/all'


class FreeProxyCZHTTPS(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/all'


class FreeProxyCZSOCKS4(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks4/ping/all'


class FreeProxyCZSOCKS5(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all'


class FreeProxyCZEliteHTTP(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/level1'


class FreeProxyCZAnonymousHTTP(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/level2'


class FreeProxyCZTransparentHTTP(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/level3'


class FreeProxyCZEliteHTTPS(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/level1'


class FreeProxyCZAnonymousHTTPS(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/level2'


class FreeProxyCZTransparentHTTPS(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/https/ping/level3'


class FreeProxyCZEliteSOCKS4(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks4/ping/level1'


class FreeProxyCZAnonymousSOCKS4(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks4/ping/level2'


class FreeProxyCZTransparentSOCKS4(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks4/ping/level3'


class FreeProxyCZEliteSOCKS5(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks5/ping/level1'


class FreeProxyCZAnonymousSOCKS5(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks5/ping/level2'


class FreeProxyCZTransparentSOCKS5(FreeProxyCZ):
    url = 'http://free-proxy.cz/en/proxylist/country/all/socks5/ping/level3'
