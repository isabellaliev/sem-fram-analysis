import requests
from bs4 import BeautifulSoup

url = "https://www.eltiempo.com/vida/educacion/dramatica-caida-en-las-habilidades-de-lectura-de-los-estudiantes-de-colombia-crecen-las-brechas-y-empeora-el-desempeno-3516549"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify()[:2000])

headline = soup.find('h1')
if headline:
        print(f"\nHeadline: {headline.text}")

paragraphs = soup.find_all('p')[:3]
for p in paragraphs:
        print(p.text)
