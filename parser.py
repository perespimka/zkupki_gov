import requests
from bs4 import BeautifulSoup
import re

url = 'http://zakupki.gov.ru/epz/orderplan/quicksearch/search.html?searchString='
ikz = re.search('/ikz (\d+)', input('Input IKZ:')).group(1)
#ikz = '193692700563469270100100040015811000'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
'Accept-Encoding':'gzip, deflate',
'Connection':'keep-alive',
'DNT':'1'
}

req = requests.get(url+ikz, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')

links = soup.find('td', class_='descriptTenderTd').find_all('a')
link_pg_calendar = 'http://zakupki.gov.ru' + links[0]['href'] #Ссыль на план-график
customer_name = links[1].string.strip() #Название заказчика

#Для ссылки на "позиции плана-графика" в конце строки должно стоять revision_id=... вместо plan-id
req_for_rev_id = requests.get(link_pg_calendar, headers=headers) 
revision_id = re.search(r'revision-id=\d+', req_for_rev_id.text).group() 
link_pg = link_pg_calendar.replace('general-information', 'search-position') #Сама ссылка на "позиции плана-графика"
link_pg = re.sub(r'plan-id=\d+', revision_id, link_pg)

req_search_pos = requests.get(link_pg, headers=headers)
soup = BeautifulSoup(req_search_pos.content, 'html.parser')
purchase_num_row = soup.find('td', title=ikz).div.parent.parent.previous_sibling.previous_sibling

print('Идентификационный код закупки: {}'.format(ikz))
print('Наименование заказчика: {}'.format(customer_name))
print('Наименование объекта закупки: {}'.format(purchase_num_row.div.label.string))







