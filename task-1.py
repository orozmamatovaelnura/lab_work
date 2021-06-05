import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd

class Wrap:
    def __init__(self,names,group,prices):
        self.readable_data = pd.DataFrame(
            {
                'Name':names,
                'Product price':prices,
                'Group':group

            }
        )

    def write_to_xlsx(self):
        writer = pd.ExcelWriter('internet_shop.xlsx', engine='xlsxwriter')
        self.readable_data.to_excel(writer, sheet_name='goods', index=False)
        writer.save()

    def write_to_csv(self):
        csvFileContents = self.readable_data.to_csv(index=False)
        with open("internet_shop.csv", "w+", encoding = 'utf-8') as f:
            f.write(csvFileContents)


def get_data(url):
    url = requests.get(url).text
    products = {
        'name':[],
        'product price':[],
        'product_class':[]
    }
    soup = BeautifulSoup(url,'html.parser')
    ads = soup.find('div', class_='list-view').find_all('div',class_='item product_listbox oh')

    for ad in ads:
        try:
            title = ad.find('div',class_='listbox_title oh').text
            products['name'].append(title)
        except:
            products['name'].append('No name')
        
        try:
            
            price = ad.find('div',class_='listbox_price text-center').text

            products['product price'].append(price)
        except:
            products['product price'].append('no price')

    aps = soup.find('div', class_='product-index product-index oh').find_all('div',class_='portlet-title')
    group = aps[0].find_all('span')
    group = group[1].text

    

    products['product_class'].append(group)

    return products


def main():
    all_names=[]
    all_prices=[]
    all_classes=[]
    url_list=['https://www.kivano.kg/elektronika','https://www.kivano.kg/kompyutery','https://www.kivano.kg/bytovaya-tekhnika','https://www.kivano.kg/avtotovary']
    for url in url_list:
        print(url,' fetching...')

        pages_part='?page='

        for i in range(1,3+1):
            url_gen = url + pages_part + str(i)
            site_data = get_data(url_gen)
            for name in site_data['name']:
                all_names.append(name)
            for link in site_data['product price']:
                all_prices.append(link)
            for i in range(len(site_data['name'])):
                all_classes.append(site_data['product_class'][0])

    goods_book = Wrap(all_names,all_classes,all_prices)

    goods_book.write_to_xlsx()
    goods_book.write_to_csv()


main()