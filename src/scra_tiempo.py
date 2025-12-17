import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_el_tiempo(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
 
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else None

        desc_tag = soup.find('meta', {'name': 'description'})
        description = desc_tag['content'] if desc_tag else None

        author_tag = soup.find('meta', {'name': 'author'})
        author = author_tag['content'] if author_tag else None 

        keywords_tag = soup.find('meta', {'name': 'keywords'})
        keywords = keywords_tag['content'] if keywords_tag else None

        full_text = f"{title}. {description}" if description else title

        return {
            'url': url,
            'title': title,
            'description': description,
            'text': author, 
            'keywords': keywords,
            'source': 'El Tiempo' 
        }
    except Exception as e:
        print(f"Error scrapping {url}: {e})")
        return None

urls = [
    "https://www.eltiempo.com/archivo/documento/CMS-16471916",
    "https://www.eltiempo.com/archivo/documento/CMS-16473749",
    "https://www.eltiempo.com/politica/proceso-de-paz/que-es-la-ley-de-amnistia-aprobada-en-el-congreso-47046",
    "https://www.eltiempo.com/justicia/cortes/cifras-de-secuestros-en-colombia-en-el-2016-42728",
    "https://www.eltiempo.com/politica/proceso-de-paz/farc-advierte-riesgo-de-impunidad-en-colombia-en-carta-a-la-cpi-1530342",
    "https://www.eltiempo.com/politica/proceso-de-paz/efectos-en-colombia-tras-un-ano-de-la-firma-del-acuerdo-de-paz-con-las-farc-152740",
    "https://www.eltiempo.com/politica/proceso-de-paz/tolima-ya-no-es-territorio-de-guerra-por-parte-de-las-farc-157682",
    "https://www.eltiempo.com/justicia/cortes/acuerdo-de-paz-con-farc-no-podra-ser-modificado-hasta-el-2030-140184",
    "https://www.eltiempo.com/politica/partidos-politicos/partido-farc-se-aparto-de-acuerdo-politico-para-modificar-la-jep-288690",
    "https://www.eltiempo.com/justicia/jep-colombia/politicos-secuestrados-por-las-farc-entregaran-testimonios-a-la-jep-284034",
    "https://www.eltiempo.com/justicia/investigacion/santrich-e-ivan-marquez-estarian-analizando-acudir-ante-la-cidh-274814",
    "https://www.eltiempo.com/justicia/jep-colombia/jep-no-encontro-a-4-exjefes-de-las-farc-para-que-ratifiquen-compromiso-con-el-proceso-272734",
    "https://www.eltiempo.com/politica/partidos-politicos/uribistas-llevaran-a-la-justicia-incumplimientos-de-los-acuerdos-de-las-farc-443042",
    "https://www.eltiempo.com/politica/proceso-de-paz/farc-rechaza-decreto-que-fija-plazo-para-entrega-de-sus-bienes-425698",
    "https://www.eltiempo.com/justicia/conflicto-y-narcotrafico/desafio-del-gobierno-para-evitar-asesinatos-de-exguerrilleros-de-las-farc-379470",
    "https://www.eltiempo.com/politica/congreso/en-votacion-de-ascensos-partido-farc-sorprendio-con-reconocimiento-al-ejercito-y-la-policia-371682",
    "https://www.eltiempo.com/politica/congreso/timochenko-dice-que-las-farc-si-han-entregado-bienes-para-la-reparacion-498356",
    "https://www.eltiempo.com/justicia/investigacion/por-que-farc-esta-reconociendo-secuestros-abusos-sexuales-y-reclutamiento-de-menores-537982",
    "https://www.eltiempo.com/politica/proceso-de-paz/que-dijeron-las-farc-en-la-comision-de-la-verdad-464718",
    "https://www.eltiempo.com/justicia/delitos/dos-excombatientes-de-farc-asesinados-el-fin-de-semana-512676", 
    "https://www.eltiempo.com/justicia/conflicto-y-narcotrafico/romana-se-arrepintio-por-victimas-de-la-guerra-y-abandono-el-acuerdo-637486", 
    "https://www.eltiempo.com/justicia/paz-y-derechos-humanos/cuantos-desaparecidos-ha-dejado-el-conflicto-en-colombia-cifras-y-datos-637170",
    "https://www.eltiempo.com/politica/proceso-de-paz/juan-manuel-santos-gobierno-desmiente-que-haya-acercamientos-con-el-eln-634535",
    "https://www.eltiempo.com/politica/proceso-de-paz/quien-es-rodrigo-granda-recorrido-por-la-vida-del-exguerrillero-626662",
    "https://www.eltiempo.com/justicia/conflicto-y-narcotrafico/comision-de-la-verdad-responsabilidad-de-guerrillas-que-azotaron-al-pais-683375",
    "https://www.eltiempo.com/colombia/otras-ciudades/campesinos-en-tumaco-impiden-presencia-de-soldados-646765", 
    "https://www.eltiempo.com/justicia/investigacion/sae-subastara-las-joyas-incautadas-a-la-extinta-guerrilla-de-las-farc-718147",
    "https://www.eltiempo.com/politica/proceso-de-paz/lafaurie-mando-a-antonio-garcia-del-eln-a-leer-acuerdos-el-no-esta-en-mesa-de-dialogo-839181",
    "https://www.eltiempo.com/justicia/investigacion/procuraduria-alerta-baja-ejecucion-de-recursos-para-implementar-el-acuerdo-de-paz-839028",
    "https://www.eltiempo.com/justicia/jep-colombia/secuestros-jep-abre-incidente-de-incumplimiento-contra-exfarc-838880",
    "https://www.eltiempo.com/politica/proceso-de-paz/los-motivos-por-los-que-el-presidente-petro-dice-que-acuerdo-de-paz-no-se-cumplira-835147",
]

articles = []
for i, url in enumerate(urls):
    print(f"Scraping {i+1}/{len(urls)}: {url}")
    article = scrape_el_tiempo(url)
    if article:
        articles.append(article)
    time.sleep(2)

df = pd.DataFrame(articles)
df.to_csv('el_tiempo_articles.csv', index=False)
print(f"\nScraped {len(df)} articles successfully!")
print(df.head())