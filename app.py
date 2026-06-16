import pandas as pd
import requests
from tqdm import tqdm
import os

os.makedirs('Imgs', exist_ok=True)

if not os.path.exists('links.csv'):
    print("Error: No se encontró el archivo 'enlaces.csv'. Por favor, crealo y volvé a intentarlo.")
    exit()

df = pd.read_csv('links.csv')

if 'img_link' not in df.columns:
    print("Error: El archivo CSV debe tener una columna llamada 'img_link'.")
    exit()

def download(link, img_path):
    try:
        res = requests.get(link, timeout=10)
        if res.status_code == 200:
            with open(img_path, 'wb') as fd:
                fd.write(res.content)
        else:
            print(f"\nNo se pudo descargar (Status: {res.status_code}): {link}")
    except Exception as e:
        print(f"\nError de conexión con el link {link}: {e}")

paths = []
img_ids = []
ref = 100000
i = 1

print(f"Iniciando la descarga de {len(df)} imágenes...")

for link in tqdm(df['img_link']):
    img_id = 'A' + str(i + ref)[1:]
    img_path = 'Imgs/' + img_id + '.jpg'

    download(link, img_path)

    paths.append(img_path)
    img_ids.append(img_id)
    i += 1

df['img_id'] = img_ids
df['img_path'] = paths

df.to_csv('links.csv', index=False)
print("¡Proceso terminado! Revisá la carpeta 'Imgs' y el archivo 'enlaces_procesados.csv'.")
