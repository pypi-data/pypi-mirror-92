from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4
import concurrent.futures


class ProxyNova(ProxyGetter):
    url = 'https://www.proxynova.com/proxy-server-list/'

    def scrap_proxy_list(self):
        scrapped = []
        urls = [self.url]
        country_list = ["us", "ca", "br", "ar", "ve", "gb", "ru", "fr",
                        "de", "pl", "ua", "cn", "hk", "jp", "tw", "kr"]
        urls += [self.url + "country-" + c for c in country_list]

        def get_url(url):
            proxies = []
            page = self.session.get(self.url, headers=self.headers)
            doc = bs4.BeautifulSoup(page.content, features="html.parser")
            for el in doc.find_all("tr"):
                try:
                    fields = [e for e in el.find_all("td")]
                    if len(fields) < 7:
                        continue
                    ip = str(fields[0]).split("document.write('")[-1].split(
                        "');</script>")[0]
                    flag = str(fields[5]).split('class="flag flag-')[-1].split(
                        " ")[0].upper()
                    last_check = str(fields[2]).split('datetime="')[-1].split(
                        '">')[0]
                    fields = [e.text.strip() for e in fields]
                    port = fields[1]
                    speed = fields[3]
                    uptime = fields[4].split("\n")[0]
                    country_name = fields[5].split("\n")[0]
                    anon = fields[-1].lower()

                    proxy_urls = {
                        "http": ip + ":" + port,
                        "https": ip + ":" + port
                    }
                    proxy_type = ProxyType.HTTP

                    if anon == "elite":
                        anon = ProxyAnonymity.ELITE
                    elif anon == "anonymous":
                        anon = ProxyAnonymity.ANONYMOUS
                    else:
                        anon = ProxyAnonymity.TRANSPARENT
                    proxies.append({"ip": ip,
                                    "port": port,
                                    "country_code": flag,
                                    "country_name": country_name,
                                    "proxy_anonymity": anon,
                                    "proxy_type": proxy_type,
                                    "ping": speed,
                                    "uptime": uptime,
                                    "urls": proxy_urls,
                                    "last_checked": last_check})
                except:
                    pass
            return proxies

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) \
                as executor:
            # scrap all port pages at same time
            future_to_port = {executor.submit(get_url, p): p for p in urls}
            for future in concurrent.futures.as_completed(future_to_port):
                scrapped += future.result()

        return scrapped


class ProxyNovaTransparent(ProxyNova):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.TRANSPARENT]


class ProxyNovaAnonymous(ProxyNova):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ANONYMOUS]


class ProxyNovaElite(ProxyNova):
    def scrap_proxy_list(self):
        proxies = super().scrap_proxy_list()
        return [p for p in proxies if
                p["proxy_anonymity"] == ProxyAnonymity.ELITE]

