import requests
from bs4 import BeautifulSoup

def print_content(content):
    # for i, c in enumerate(content):
    #     print(f'{i+1}: {c}')
    for c in content:
        print(c.text)
        
def print_autos(autos):
    for auto in autos:
        print(f"Precio: {auto['precio']}")
        print(f"Año: {auto['anio']}")
        print(f"Kilometraje: {auto['kilometraje']}")
        print(f"Modelo: {auto['modelo']}")
        print(f"Ubicación: {auto['ubicacion']}")
        print(f"Vendedor: {auto['vendedor']}")
        print("-" * 50)

# URL de la página web que deseas scrapear
url = 'https://autos.mercadolibre.cl/chevrolet/'

# Realiza una solicitud HTTP GET a la URL
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Extrae el contenido HTML de la respuesta
    html_content = response.content

    # Crea un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html_content, 'lxml')

    information_elements = soup.find_all('div', class_='ui-search-result__content')
    # Lista para almacenar los datos estructurados
    autos = []
    # print_content(information_element)
    for element in information_elements:
        precio = element.find('span', class_='andes-money-amount__fraction').text
        detalles = element.find('ul', class_='ui-search-card-attributes ui-search-item__group__element')
        
        # A veces los detalles pueden no estar bien formateados o no ser consistentes
        if detalles:
            detalles_list = detalles.find_all('li')
            if len(detalles_list) >= 2:
                anio = detalles_list[0].text.strip()
                kilometraje = detalles_list[1].text.strip()
            else:
                anio = kilometraje = 'N/A'
        else:
            anio = kilometraje = 'N/A'

        modelo = element.find('h2', class_='ui-search-item__title').text
        ubicacion = element.find('span', class_='ui-search-item__location').text if element.find('span', class_='ui-search-item__location') else 'N/A'
        vendedor = element.find('p', class_='ui-search-official-store-label ui-search-item__group__element ui-search-color--GRAY').text if element.find('p', class_='ui-search-official-store-label ui-search-item__group__element ui-search-color--GRAY') else 'Individual'

        auto = {
            'precio': precio,
            'anio': anio,
            'kilometraje': kilometraje,
            'modelo': modelo,
            'ubicacion': ubicacion,
            'vendedor': vendedor
        }
        autos.append(auto)

    # Imprime los datos estructurados
    print_autos(autos)

else:
    print("Error al obtener la página:", response.status_code)
