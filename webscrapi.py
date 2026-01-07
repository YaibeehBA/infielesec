import requests
import json
import time
from typing import List, Dict, Optional
import pandas as pd

class RNIGraphQLScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    
    def fetch_historias(self, limit: int = 100, offset: int = 0) -> Optional[Dict]:
        """
        Hace una petición al endpoint GraphQL para obtener historias
        """
        # Query GraphQL para  la estructura la API
        query = """
        query GetHistorias($limit: Int, $offset: Int) {
            historias(limit: $limit, offset: $offset) {
                _id
                infiel {
                    _id
                    primer_nombre
                    iniciales_apellidos
                    sexo
                    edad
                    provincia
                    canton
                    parroquia
                }
                historia_filtrada
                tiempo_meses
                tipo_infiel
                reputacion {
                    tipo
                    votos
                }
                total_reacciones
                reacciones_list {
                    tipo
                    cantidad
                }
                fecha_registro_timestamp
            }
        }
        """
        
        payload = {
            "query": query,
            "variables": {
                "limit": limit,
                "offset": offset
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            return None
    
    def scrape_all_historias(self, batch_size: int = 100, max_records: int = None) -> List[Dict]:
        """
        Obtiene todas las historias disponibles mediante paginación
        """
        all_historias = []
        offset = 0
        
        while True:
            print(f"Obteniendo registros desde offset {offset}...")
            
            data = self.fetch_historias(limit=batch_size, offset=offset)
            
            if not data or 'data' not in data:
                print("No se obtuvieron más datos")
                break
            
            historias = data.get('data', {}).get('historias', [])
            
            if not historias:
                print("No hay más historias disponibles")
                break
            
            all_historias.extend(historias)
            print(f"Total acumulado: {len(all_historias)} historias")
            
            # Si llegamos al máximo deseado
            if max_records and len(all_historias) >= max_records:
                all_historias = all_historias[:max_records]
                break
            
            offset += batch_size
            time.sleep(1)  # Pausa para no saturar el servidor
        
        return all_historias
    
    def flatten_data(self, historias: List[Dict]) -> List[Dict]:
        """
        Aplana los datos anidados para facilitar el análisis
        """
        flattened = []
        
        for historia in historias:
            flat_record = {
                'historia_id': historia.get('_id'),
                'infiel_id': historia.get('infiel', {}).get('_id'),
                'primer_nombre': historia.get('infiel', {}).get('primer_nombre'),
                'iniciales_apellidos': historia.get('infiel', {}).get('iniciales_apellidos'),
                'sexo': historia.get('infiel', {}).get('sexo'),
                'edad': historia.get('infiel', {}).get('edad'),
                'provincia': historia.get('infiel', {}).get('provincia'),
                'canton': historia.get('infiel', {}).get('canton'),
                'parroquia': historia.get('infiel', {}).get('parroquia'),
                'historia_filtrada': historia.get('historia_filtrada'),
                'tiempo_meses': historia.get('tiempo_meses'),
                'tipo_infiel': historia.get('tipo_infiel'),
                'reputacion_tipo': historia.get('reputacion', {}).get('tipo'),
                'reputacion_votos': historia.get('reputacion', {}).get('votos'),
                'total_reacciones': historia.get('total_reacciones'),
                'fecha_registro_timestamp': historia.get('fecha_registro_timestamp'),
            }
            
            # Agregar reacciones como columnas separadas
            reacciones = historia.get('reacciones_list', [])
            for reaccion in reacciones:
                tipo = reaccion.get('tipo', 'UNKNOWN')
                cantidad = reaccion.get('cantidad', 0)
                flat_record[f'reaccion_{tipo}'] = cantidad
            
            flattened.append(flat_record)
        
        return flattened
    
    def save_to_json(self, data: List[Dict], filename: str = 'historias_raw.json'):
        """Guarda los datos en formato JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Datos guardados en {filename}")
    
    def save_to_csv(self, data: List[Dict], filename: str = 'historias.csv'):
        """Guarda los datos en formato CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Datos guardados en {filename}")
    
    def save_to_excel(self, data: List[Dict], filename: str = 'historias.xlsx'):
        """Guarda los datos en formato Excel"""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Datos guardados en {filename}")


# Uso del scraper
if __name__ == "__main__":
    # URL del endpoint
    url = "https://backend-rni-vzlovy3u4a-rj.a.run.app/graphql"
    
    # Crear instancia del scraper
    scraper = RNIGraphQLScraper(url)
    
    # Opción 1: Obtener todas las historias
    print("Iniciando scraping...")
    historias = scraper.scrape_all_historias(batch_size=100)
    
    # Opción 2: Obtener un máximo de registros
    # historias = scraper.scrape_all_historias(batch_size=100, max_records=1000)
    
    print(f"\nTotal de historias obtenidas: {len(historias)}")
    
    if historias:
        # Guardar datos sin procesar
        scraper.save_to_json(historias, 'historias_raw.json')
        
        # Aplanar y guardar en diferentes formatos
        flat_data = scraper.flatten_data(historias)
        scraper.save_to_csv(flat_data, 'historias.csv')
        
        
        try:
            scraper.save_to_excel(flat_data, 'historias.xlsx')
        except Exception as e:
            print(f"No se pudo guardar en Excel: {e}")
        
        # Mostrar estadísticas básicas
        print("\n=== Estadísticas ===")
        df = pd.DataFrame(flat_data)
        print(f"Provincias únicas: {df['provincia'].nunique()}")
        print(f"Distribución por sexo:\n{df['sexo'].value_counts()}")
        print(f"Edad promedio: {df['edad'].mean():.1f} años")