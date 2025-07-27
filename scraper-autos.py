import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

def print_content(content):
    # for i, c in enumerate(content):
    #     print(f'{i+1}: {c}')
    for c in content:
        print(c.text)
        
def print_autos(autos):
    for auto in autos:
        print(f"id: {auto['id']}")
        print(f"Precio: {auto['precio']}")
        print(f"Año: {auto['anio']}")
        print(f"Kilometraje: {auto['kilometraje']}")
        print(f"Modelo: {auto['modelo']}")
        print(f"Ubicación: {auto['ubicacion']}")
        print(f"Vendedor: {auto['vendedor']}")
        print(f"URL: {auto['url']}")
        print("-" * 50)

#lista de marcas registradas en Mercadolibre
# marcas_list = ["chevrolet", "peugeot", "nissan", "ford", "hyundai", "kia", "volkswagen", "toyota", "bMW", "suzuki", "mazda", "mg", "mercedes-benz",
#                  "honda", "jeep", "mitsubishi", "subaru", "ssangyong", "renault", "audi", "citroen", "fiat", "volvo", "changan", "opel", "chery", 
#                  "ram", "fiat", "jac", "land-rover", "haval", "maxus", "dodge", "geely", "porsche", "great-wall", "mini", "porsche"]


# Arreglo de prueba con solo 3 marcas
marcas_list = ["chevrolet", "peugeot", "nissan"]

# Lista de user agents para simular diferentes navegadores
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
]

# Lista para almacenar todos los autos de todas las marcas
all_autos = []

for marca in marcas_list:
    # Inicializa el índice de la página en 1
    i=0
    index_show = 48 # Número de resultados por página
    
    resultados_marca = 0
    while i < 10:
        # Calcula la URL para la página actual
        calculate_index = i*index_show+1 
        # URL de la página de búsqueda de autos en Mercadolibre para la marca actual
        url = f'https://autos.mercadolibre.cl/{marca}/_Desde_{calculate_index}_NoIndex_True'
        # Define los encabezados de la solicitud para simular un navegador aleatorio
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url, headers=headers)
        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            #revisar el caso base sin index
            # Extrae el contenido HTML de la respuesta
            html_content = response.content

            # Crea un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html_content, 'lxml')

            # Busca los elementos que contienen la información deseada
            information_elements = soup.find_all('li', class_='ui-search-layout__item')
       
            # Si no se encuentran elementos, termina el bucle caso base
            if len(information_elements) == 0:
                print("No hay más datos para scrapear")
                break
            # Lista para almacenar los datos estructurados
            autos = []
        
            # Itera sobre los elementos encontrados y extrae la información deseada
            for element in information_elements:
                # Buscar el enlace del auto
                a_tag = element.find('a', class_='poly-component__title')
                if not a_tag or not a_tag.has_attr('href'):
                    continue
                link = a_tag['href']
                # Extraer el id del auto desde el enlace
                try:
                    id = link.split('-')[1]
                except Exception:
                    id = 'N/A'

                # Precio
                precio_tag = element.find('span', class_='andes-money-amount__fraction')
                precio = precio_tag.text.strip() if precio_tag else 'N/A'

                # Modelo
                modelo_tag = a_tag
                modelo = modelo_tag.text.strip() if modelo_tag else 'N/A'

                # Año y kilometraje
                anio = kilometraje = 'N/A'
                detalles_ul = element.find('ul', class_='poly-attributes_list')
                if detalles_ul:
                    detalles_list = detalles_ul.find_all('li')
                    if len(detalles_list) >= 2:
                        anio = detalles_list[0].text.strip()
                        kilometraje = detalles_list[1].text.strip()

                # Ubicación
                ubicacion_tag = element.find('span', class_='poly-component__location')
                ubicacion = ubicacion_tag.text.strip() if ubicacion_tag else 'N/A'

                # Vendedor
                vendedor_tag = element.find('span', class_='poly-component__seller')
                if vendedor_tag:
                    vendedor = vendedor_tag.text.strip().replace('Por ', '')
                else:
                    vendedor = 'Individual'

                auto = {
                    'id': id,
                    'url': link,
                    'precio': precio,
                    'anio': anio,
                    'kilometraje': kilometraje,
                    'modelo': modelo,
                    'ubicacion': ubicacion,
                    'vendedor': vendedor
                }
                autos.append(auto)
                all_autos.append(auto)

            # Imprime los datos estructurados
            # print(" ------------------------- Datos estructurados: -------------------------")
            print_autos(autos)
            # print(calculate_index)
            i += 1
       

        else:
            print("Error al obtener la página:", response.status_code)

# Crear un DataFrame de pandas con todos los autos y guardarlo en un archivo Excel
df = pd.DataFrame(all_autos)
df.to_excel('autos_mercadolibre.xlsx', index=False)

print("Datos guardados en autos_mercadolibre.xlsx")
