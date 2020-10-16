from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
from switchcase import switch

sites = [["bazargarm","okala","sunmiveh"],['https://www.bazargam.com/Fruit?s=120','https://okala.com/fresh-fruits-vegetables/fresh-fruit',
          'https://sunmiveh.com/%D9%85%DB%8C%D9%88%D9%87']]

def crawler(name, url):

    for case in switch(name):

        if case("bazargarm"):
            uClient = uReq(url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("div", {"class": "artDiv"})

            with open("bazargarm.csv", "w", encoding='utf-8') as csvFile:
                fieldnames = ["discount", "item", "weight", "price", "old_price"]
                writer = csv.writer(csvFile)
                writer.writerow(fieldnames)

                for container in containers:
                    a = container.find("div", {"class": "art-badges"}).find("span", {"class": "art-badge"}).string.strip()
                    b = container.find_all("div", {"class": "art-data-block"})[1]
                    b1 = b.div.div.string.strip()
                    b2 = b.find("div", {"class": "art-info-block"}).h3.a.span.string.strip()
                    c = container.find("div", {"class": "art-drop1"})
                    c1 = c.div.div.span.string.strip()
                    c2 = c.find_all("div", {"class": "row no-gutters"})[1].span.string.strip()
                    fields = [a, b1, b2, c1, c2]
                    writer.writerow(fields)

        if case("okala"):
            with open("okala.csv", "w", encoding='utf-8') as csvFile:
                fieldnames = ["item", "old_price", "price"]
                writer = csv.writer(csvFile)
                writer.writerow(fieldnames)

                for j in range(1, 5):
                    uClient = uReq(url + "?pageNumber=%d" % j)
                    page_html = uClient.read()
                    uClient.close()
                    page_soup = soup(page_html, "html.parser")
                    containers = page_soup.findAll("div", {"class": "product-box product-box_hover"})

                    for container in containers:
                        a = container.find("a", {"class": "product-box_title text-dark"}).text
                        b = container.find("div", {"class": "product-box_content"}).a.find_all()
                        b1 = b[0].text
                        try:
                            b2 = b[1].text
                        except:
                            pass
                        fields = [a, b1, b2]
                        writer.writerow(fields)
        if case("sunmiveh"):
            with open("sunmiveh.csv", "w", encoding='utf-8') as csvFile:
                fieldnames = ["item", "lux_price", "momtaz_price", "Khanevar_price"]
                writer = csv.writer(csvFile)
                writer.writerow(fieldnames)

                for j in range(1, 3):
                    uClient = uReq(url + "?page=%d" % j)
                    page_html = uClient.read()
                    uClient.close()
                    page_soup = soup(page_html, "html.parser")
                    containers = page_soup.findAll("div", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-2"})

                    for container in containers:
                        a = container.a.find("h6", {"class": "store-name ptb-10 posts-nav"}).text
                        b = container.findAll("h6", {"class": "store-name ptb-10"})
                        try:
                            b1 = re.findall('\d+',b[0].span.text)
                            b1o = ''.join(b1)
                            b2 = re.findall('\d+',b[1].span.text)
                            b2o = ''.join(b2)
                            b3 = re.findall('\d+',b[2].span.text)
                            b3o = ''.join(b3)
                        except:
                            pass
                        fields = [a, b1o, b2o, b3o]
                        writer.writerow(fields)

    return

for i in range (len(sites[0])):

    crawler(sites[0][i],sites[1][i])

print("Successful! grab your CSVs")