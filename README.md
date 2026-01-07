# 📊 Análisis de Datos: Registro Nacional de Infieles (RNI) - Ecuador

## 📋 Descripción del Proyecto

Análisis de datos del **Registro Nacional de Infieles (RNI)** del Ecuador, obtenidos mediante web scraping de una API GraphQL. El proyecto incluye extracción, limpieza, estandarización y análisis exploratorio de casos de infidelidad reportados en el país.

## 🎯 Objetivos

- Extraer datos estructurados sobre casos de infidelidad mediante web scraping
- Realizar limpieza y estandarización de datos geográficos y demográficos
- Identificar patrones y tendencias en el comportamiento de infieles
- Generar visualizaciones y métricas para análisis cualitativo y cuantitativo

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**
- **Librerías principales**:
  - `requests` - Peticiones HTTP a la API GraphQL
  - `pandas` - Manipulación y análisis de datos
  - `json` - Manejo de datos JSON
  - `time` - Control de pausas entre peticiones

## 📊 Estructura de Datos

### Datos Obtenidos (25 columnas):

#### **Información Demográfica:**
- `historia_id` - Identificador único de la historia
- `infiel_id` - Identificador único del infiel
- `primer_nombre` - Nombre del infiel
- `iniciales_apellidos` - Iniciales de apellidos
- `sexo` - Género (M/F)
- `edad` - Edad del infiel
- `provincia` - Provincia de residencia
- `canton` - Cantón de residencia
- `parroquia` - Parroquia de residencia

#### **Información de la Infidelidad:**
- `historia_filtrada` - Descripción de la historia
- `tiempo_meses` - Duración en meses
- `tipo_infiel` - Categorización del infiel
- `fecha_registro_timestamp` - Fecha de registro

#### **Reputación y Reacciones:**
- `reputacion_tipo` - Tipo de reputación
- `reputacion_votos` - Cantidad de votos
- `total_reacciones` - Total de reacciones
- `reaccion_PISHCOTA` - Reacción "Pishcota"
- `reaccion_QUEMONA` - Reacción "Quemona"
- `reaccion_DESGRACIADO` - Reacción "Desgraciado"
- `reaccion_PRINCIPIANTE` - Reacción "Principiante"
- `reaccion_SINVERGUENZA` - Reacción "Sinvergüenza"
- `reaccion_MOJIGATA` - Reacción "Mojigata"
- `reaccion_SANGRONA` - Reacción "Sangrona"
- `reaccion_MAESTRO` - Reacción "Maestro"
- `reaccion_PICADA` - Reacción "Picada"
- `reaccion_MACHO_ALFA` - Reacción "Macho Alfa"

## 🔄 Proceso de Extracción

### 1. **Web Scraping con GraphQL**
```python
# Configuración del scraper
scraper = RNIGraphQLScraper("https://backend-rni-vzlovy3u4a-rj.a.run.app/graphql")
historias = scraper.scrape_all_historias(batch_size=100)
