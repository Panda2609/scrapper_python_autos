# Scraper de Autos MercadoLibre

Este proyecto es un script en Python para scrapear información de autos publicados en [MercadoLibre Chile - Autos](https://autos.mercadolibre.cl/). Extrae datos como modelo, precio, año, kilometraje, ubicación, vendedor y URL de cada publicación, y los guarda en un archivo Excel.

## Requisitos
- Python 3.7+
- Paquetes: `requests`, `beautifulsoup4`, `pandas`, `lxml`

Puedes instalar los paquetes necesarios con:

```
pip install requests beautifulsoup4 pandas lxml
```

## Uso
1. Clona este repositorio o descarga el archivo `scraper-autos.py`.
2. Ejecuta el script:
   ```
   python scraper-autos.py
   ```
3. El script generará un archivo `autos_mercadolibre.xlsx` con los resultados.

## Personalización
- Por defecto, el script usa solo 3 marcas para pruebas rápidas. Puedes cambiar la lista `marcas_list` para scrapear todas las marcas disponibles. Puedes agregar más marcas o eliminar marcas existentes. Tener en consideración que se demorará más tiempo si intentas scrapear todas las marcas, ya que es una busqueda lineal.

- El script simula diferentes navegadores usando varios user agents aleatorios para evitar bloqueos.
- El scraping se detiene después de 10 páginas por marca para evitar bucles infinitos.

## Notas
- El scraping de sitios web puede estar sujeto a cambios en la estructura del HTML. Si el script deja de funcionar, revisa si MercadoLibre ha cambiado su diseño.
- Usa este script solo para fines educativos y respeta los términos de uso de MercadoLibre.

