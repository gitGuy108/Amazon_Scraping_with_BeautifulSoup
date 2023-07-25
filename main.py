import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# PART 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

url_list = [
    'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=2&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=3&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=4&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=5&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=6&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=7&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=8&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=9&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=10&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=11&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=12&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=13&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=14&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=15&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=16&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=17&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=18&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=19&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
    'https://www.amazon.in/s?k=bags&page=20&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
]
base_url = 'https://www.amazon.in/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
          'referer': 'https://www.google.com/'}


def getdata(link):
    site_info = requests.get(link, headers=header)
    status = site_info.status_code
    print(status)

    if status == 200:
        html_text = site_info.text
        return html_text
    else:
        return getdata(link)


with open('Product_List/product_list.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)

    for url in url_list:
        content = getdata(url)

        soup = BeautifulSoup(content, 'lxml')
        product_div = soup.find_all('div',
                                    class_="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right")

        for index in range(len(product_div)):
            product_name = product_div[index].div.div.div.h2.a.span.text
            relative_url = product_div[index].div.div.div.h2.a['href']
            product_url = urljoin(base_url, relative_url)

            try:
                product_price = product_div[index].find('span', class_="a-price-whole").text
            except AttributeError:
                product_price = 'NA'

            print(product_name)
            print(product_url)
            print("Price:" + product_price)

            try:
                rating_element = product_div[index].find('div', class_="a-row a-size-small")

                product_rating = rating_element.select('span[aria-label]')[0]['aria-label']
                product_reviews = rating_element.select('span[aria-label]')[1]['aria-label']
            except AttributeError:
                product_rating = 'NA'
                product_reviews = 'NA'

            print(product_rating)
            print("Total Reviews:" + product_reviews)
            print("")

            csv_row = [product_url, product_name, product_price, product_rating, product_reviews]
            writer.writerow(csv_row)


# PART 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


with open('Information_of_Products/products.csv', 'w', encoding="utf-8", newline='') as new_file:
    writer = csv.writer(new_file)

    with open('Product_List/product_list.csv', 'r') as pro_list:
        csv_f = csv.reader(pro_list)
        for row in csv_f:
            product_url = row[0]

            product_page_html = getdata(product_url)

            soup1 = BeautifulSoup(product_page_html, 'lxml')
            product_title = soup1.find('span', id="productTitle").text.strip()

            print("Product: " + product_title)

            try:
                ASIN_element = soup1.find(lambda tag: tag.name == "span" and "ASIN" in tag.text)
                if not ASIN_element:
                    ASIN_element = soup1.find(lambda tag: tag.name == "th" and "ASIN" in tag.text).parent
                    product_ASIN = ASIN_element.td.text
                else:
                    product_ASIN = ASIN_element.find_all('span')[1].text
            except AttributeError:
                product_ASIN = 'NA'
            print("ASIN: " + product_ASIN)

            try:
                base_element = soup1.find(lambda tag: tag.name == "th" and "Manufacturer" in tag.text)
                if not base_element:
                    # print(soup1.find_all(lambda tag: tag.name == "span" and "Manufacturer" in tag.text))
                    Manufacturer_element = soup1.find_all(lambda tag: tag.name == "span" and "Manufacturer" in tag.text)[-2]
                    # print("firstcase: " + str(Manufacturer_element))
                    product_Manufacturer = Manufacturer_element.find_all('span')[1].text
                else:
                    Manufacturer_element = base_element.parent
                    # print("secondcase: " + str(Manufacturer_element))
                    product_Manufacturer = Manufacturer_element.td.text.strip()
            except (AttributeError, IndexError) as error:
                # print(error)
                product_Manufacturer = 'NA'
            print("Manufacturer: " + product_Manufacturer)

            try:
                product_desc = soup1.find('div', id="productDescription").p.span.text
            except AttributeError:
                product_desc = 'NA'
            print("Description: " + product_desc)
            print('')

            writer.writerow([product_title, product_ASIN, product_Manufacturer, product_desc])
