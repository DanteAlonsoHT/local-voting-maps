import re

def extraer_secciones(text):
    # Expresiones regulares para identificar intervalos y números individuales
    range_pattern = r'de la (\d+) a la (\d+)'  # Captura "de la X a la Y"
    single_pattern = r', (\d+),'               # Captura ", Z,"

    numbers = []

    # Buscar intervalos y expandirlos
    for start, end in re.findall(range_pattern, text):
        numbers.extend(range(int(start), int(end) + 1))

    # Buscar números individuales
    for number in re.findall(single_pattern, text):
        numbers.append(int(number))

    # Para capturar números al final de las frases, separados por comas o puntos
    extra_numbers = re.findall(r'(?:,| )(\d+)(?:,|\.| y)', text)
    for number in extra_numbers:
        num = int(number)
        if num not in numbers:  # Evitar duplicados
            numbers.append(num)

    return [str(i) for i in sorted(numbers)]
    #numeros_como_strings = list(map(str, numeros_ints))
    #return numeros_como_strings

# Archivos CSV de votaciones
voting_files = ['./WhatToUpload/GTO_AYUN_24.csv', './WhatToUpload/GTO_DIP_LOC_24.csv', './WhatToUpload/GTO_GUB_24.csv']
shapefile_path = './WhatToUpload/SECCION.shp'

file_names = ["Ayuntamiento GTO", "Diputaciones Locales GTO", "Gubernamentales GTO"]

rate_column_names = ['TASA_VOTOS_PAN',	'TASA_VOTOS_MORENA', 'Distrito']

columns_to_clean = ['TOTAL_VOTOS_CALCULADO','PAN','PRI', 'PRD', 'MORENA']
politic_partys = ['PAN', 'PRI', 'PRD', 'MORENA', ['PAN', 'PRI', 'PRD']]

columns_to_show_in_table = ['SECCION', 'TOTAL_VOTOS_CALCULADO'] + rate_column_names[:-1]

texto_distritos_iv = '''secciones: de la 1275 a la 1277, de la 1284 a la 1285,
de la 1296 a la 1301, de la 1306 a la 1311, 1322, 1343, 1367,
de la 1390 a la 1391, 1393, de la 1412 a la 1413, de la 1474 a la 1476, 1479,
de la 1481 a la 1482, de la 1485 a la 1489, 1495, de la 1497 a la 1499,
de la 1503 a la 1506, de la 1508 a la 1510, de la 1512 a la 1513, 1654,
de la 1660 a la 1661, de la 3031 a la 3041, 3044, de la 3046 a la 3047, 3051,
de la 3071 a la 3101, 3131, de la 3133 a la 3142, y
de la 3149 a la 3154.'''

texto_distritos_v = '''secciones: de la 1464 a la 1467, de la 1483 a la 1484,
de la 1490 a la 1494, de la 1721 a la 1724, de la 1731 a la 1734, 1739,
de la 1741 a la 1742, de la 1747 a la 1748, de la 1750 a la 1754, 1765,
de la 1767 a la 1771, de la 1773 a la 1775, de la 1782 a la 1784, 1787,
de la 1794 a la 1797, 1803, de la 1807 a la 1810, de la 1813 a la 1814, 1818,
de la 1823 a la 1824, de la 1827 a la 1828, de la 1832 a la 1836,
de la 1838 a la 1841, de la 1846 a la 1847, 1850, de la 1854 a la 1855,
de la 1857 a la 1858, y de la 3006 a la 3030.'''

secciones_distritos_iv = extraer_secciones(texto_distritos_iv)
secciones_distritos_v = extraer_secciones(texto_distritos_v)
