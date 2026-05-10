import os
import requests
import concurrent.futures

# Nombre de la carpeta donde se guardarán los logos
CARPETA_DESTINO = "logos_izzi"

# Crear la carpeta si no existe en el directorio actual
if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO)

def descargar_logo(channel_id):
    url = f"https://www.izzigo.tv/images/ch/{channel_id}/LOGO/m/0"
    try:
        # Usamos GET para obtener el archivo completo
        respuesta = requests.get(url, timeout=5)
        
        # Verificamos que la petición sea exitosa (código 200)
        if respuesta.status_code == 200:
            # Construimos la ruta del archivo asegurando la extensión .png
            ruta_archivo = os.path.join(CARPETA_DESTINO, f"{channel_id}.png")
            
            # Escribimos los bytes de la imagen en el archivo local
            with open(ruta_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            
            return channel_id, True
    except requests.RequestException:
        pass
    
    return channel_id, False

def procesar_canales(limite=3000):
    descargados = 0
    print(f"Iniciando escaneo y descarga de {limite} IDs...")
    print(f"Los logos válidos se guardarán en: ./{CARPETA_DESTINO}/\n")
    
    # Hacemos las peticiones concurrentes para agilizar la descarga
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        resultados = executor.map(descargar_logo, range(1, limite + 1))
        
        for ch_id, exito in resultados:
            if exito:
                print(f"[+] Descargado exitosamente: {ch_id}.png")
                descargados += 1

    print(f"\nProceso terminado. Se descargaron {descargados} logos en total.")

if __name__ == "__main__":
    # Escanear del ID 1 al 3000
    procesar_canales(3000)