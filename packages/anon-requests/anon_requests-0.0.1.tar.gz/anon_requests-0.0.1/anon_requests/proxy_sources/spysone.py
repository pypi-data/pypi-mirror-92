from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4
import concurrent.futures


class SpysOne(ProxyGetter):
    url = 'https://spys.one/proxy-port/'

    def scrap_proxy_list(self):

        # top 32 ports
        top32 = ["8080", "3128", "1080", "80", "999", "5836", "9999",
                 "53281", "8118", "8888", "3838", "9050", "8081",
                 "9090", "6667", "4216", "23500", "9991", "83", "4145",
                 "55443", "6666", "8000", "3000", "443", "3129", "808",
                 "1081", "8090", "8181", "82", "8902"]

        def get_port(port):
            proxies = []
            page = self.session.get(self.url + port, headers=self.headers)
            doc = bs4.BeautifulSoup(page.content, features="html.parser")
            for el in doc.find_all("tr"):
                fields = [e.text for e in el.find_all("td")]
                if len(fields) < 9:
                    continue
                if not fields[0][0].isdigit():
                    continue
                ip = fields[0].split(":")[0]
                proxy_urls = {
                    "http":  ip + ":" + port,
                    "https":  ip + ":" + port
                }
                proxy_type = ProxyType.HTTP
                if "https" in fields[1].lower():
                    proxy_type = ProxyType.HTTPS
                elif "socks5" in fields[1].lower():
                    proxy_type = ProxyType.SOCKS5
                elif "socks4" in fields[1].lower():
                    proxy_type = ProxyType.SOCKS4

                if fields[2] == "HIA":
                    anon = ProxyAnonymity.ELITE
                elif fields[2] == "ANM":
                    anon = ProxyAnonymity.ANONYMOUS
                else:
                    anon = ProxyAnonymity.TRANSPARENT
                uptime = fields[-2].split("%")[0] + "%"
                proxies.append({"ip": ip,
                                "port": port,
                                "country_code": fields[3],
                                "proxy_anonymity": anon,
                                "proxy_type": proxy_type,
                                "urls": proxy_urls,
                                "host": fields[4],
                                "latency": fields[5],
                                "uptime": uptime,
                                "last_checked": fields[-1]})
            return proxies

        scrapped = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) \
                as executor:
            # scrap all port pages at same time
            future_to_port = {executor.submit(get_port, p): p for p in top32}
            for future in concurrent.futures.as_completed(future_to_port):
                scrapped += future.result()

        return scrapped
