from bs4 import BeautifulSoup
import requests
import pandas as pd

ebit_WIG20 = 'https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/indeks:WIG20,Y,IncomeEBIT,2,2,0'
ebit_html = requests.get(ebit_WIG20).text
soup_eb = BeautifulSoup(ebit_html, 'lxml')
data_ebit = soup_eb.find_all('tr')[1:]
Name_li = []
EBIT_li = []
dict_ebit = {'Name': Name_li, 'EBIT': EBIT_li}
for i in data_ebit:
    company_name = i.find('a').text
    Name_li.append(company_name)
    company_ebit = i.find('span', class_='pv').span.text.replace(" ", "")
    EBIT_li.append(company_ebit)
ebit = pd.DataFrame(dict_ebit)

amortisation_WIG20 = 'https://www.biznesradar.pl/spolki-raporty-finansowe-przeplywy-pieniezne/indeks:WIG20,Y,CashflowAmortization'
amortisation_html = requests.get(amortisation_WIG20).text
soup_am = BeautifulSoup(amortisation_html, 'lxml')
data_amortisation = soup_am.find_all('tr')[1:]
Name2_li = []
amortisation_li = []
dict_amortisation = {'Name': Name2_li, 'Amortisation': amortisation_li}
for i in data_amortisation:
    company_name2 = i.find('a').text
    Name2_li.append(company_name2)
    company_amortisation = i.find('span', class_='pv').span.text.replace(" ", "")
    amortisation_li.append(company_amortisation)
amortisation = pd.DataFrame(dict_amortisation)

df_merged = ebit.merge(amortisation, on='Name')
df_merged['EBIT'] = pd.to_numeric(df_merged['EBIT'])
df_merged['Amortisation'] = pd.to_numeric(df_merged['Amortisation'])
df_merged['EBITDA'] = df_merged['EBIT'] + df_merged['Amortisation']

EBITDA = df_merged.drop(columns=['EBIT', 'Amortisation'])
EBITDA.set_index('Name', inplace=True)
print(EBITDA)
