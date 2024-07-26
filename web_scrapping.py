import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree

# Petición al server
url = 'https://elpais.com/'
response = requests.get(url)

if response.status_code == 200:
    print(f"Descargado correctamente {url}")
else:
    print(f"Error en la descarga de la web {url}, con código de error: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')
titulos_h2 = soup.find_all('h2', class_='c_t')
for i, titulo in enumerate(titulos_h2, start = 1):
    print(f"{i}. {titulo.get_text(strip=True)}")

del(i, titulo, titulos_h2) # pendiente de eliminar url, response, soup

def extraer_noticias(soup):
    noticias = [] 
    secciones = soup.find_all('section', class_ = 'b-t') # secciones de noticias a buscar

    for seccion in secciones:
        articulos = seccion.find_all('article')
        for articulo in articulos:
            #extraer el título
            titulo_tag = articulo.find('h2', class_ = 'c_t')
            if titulo_tag:
                titulo = titulo_tag.get_text(strip = True)
            else:
                titulo = "Titulo no disponible en el parseo"

            # extraer el resumen
            resumen_tag = articulo.find('p', class_ = 'c_d')
            if resumen_tag:
                resumen = resumen_tag.get_text(strip = True)
            else:
                resumen = "Resumen no disponible en el parseo"
            
            # extraer el enlace
            enlace_tag = articulo.find('a', class_ = 'c_d')
            if enlace_tag:
                enlace = enlace_tag['href']
                if not enlace.startswith('http'):
                    enlace = 'https://elpais.com/' + enlace
            else: 
                enlace = 'Enlace no disponible en el parseo'

            # Añadir noticia al contenedor
            noticias.append({
                'titulo':titulo,
                'resumen':resumen,
                'enlace':enlace
            })
    
    return noticias

noticias = extraer_noticias(soup)
print(noticias)