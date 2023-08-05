from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4


class ProxyScan(ProxyGetter):
    url = 'https://www.proxyscan.io'

    def scrap_proxy_list(self):
        proxies = []
        page = self.session.get(self.url, headers=self.headers)
        doc = bs4.BeautifulSoup(page.content, features="html.parser")
        for el in doc.find_all("tr"):
            try:
                fields = [e.text for e in el.find_all("td")]
                if len(fields) < 5:
                    continue
                ip = el.find("th").text
                port = fields[0]
                proxy_type = fields[3].lower().strip()
                country_name, city = fields[1].strip().split(",")
                ping = fields[2].strip()
                anon = fields[4]
                uptime = fields[5]
                ts = fields[-1]
                flag = str(el.find("span")).split("flag-icon flag-icon-")[
                    -1].split('"')[0].upper()

                proxy_urls = {
                    "http": ip + ":" + port,
                    "https": ip + ":" + port
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
                                "city": city.strip(),
                                "proxy_anonymity": anon,
                                "proxy_type": proxy_type,
                                "ping": ping,
                                "uptime": uptime,
                                "urls": proxy_urls,
                                "last_checked": ts})
            except:
                pass
        return proxies


class ProxyScanHTTPS(ProxyScan):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if p["proxy_type"] == ProxyType.HTTPS]


class ProxyScanSOCKS4(ProxyScan):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if p["proxy_type"] == ProxyType.SOCKS4]


class ProxyScanSOCKS5(ProxyScan):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if p["proxy_type"] == ProxyType.SOCKS5]


class ProxyScanAnonymous(ProxyScan):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class ProxyScanElite(ProxyScan):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]


class ProxyScanHTTPSAnonymous(ProxyScanHTTPS):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class ProxyScanHTTPSElite(ProxyScanHTTPS):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]


class ProxyScanSOCK4Anonymous(ProxyScanSOCKS4):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class ProxyScanSOCKS4Elite(ProxyScanSOCKS4):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]


class ProxyScanSOCKS5Anonymous(ProxyScanSOCKS5):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class ProxyScanSOCKS5Elite(ProxyScanSOCKS5):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]
