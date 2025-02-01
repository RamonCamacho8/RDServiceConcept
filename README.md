# Proyecto POC - Pipeline de Procesamiento de Imágenes

Este proyecto es una prueba de concepto que implementa un pipeline de procesamiento de imágenes utilizando un cliente en React y un servidor en FastAPI con Celery y ReportLab.

## Funcionalidades

### Cliente
- **Carga de imágenes:** Permite subir una o más imágenes.
- **Previsualización:** Muestra una vista previa de las imágenes subidas.
- **Envío de imágenes:** Envía las imágenes al servidor.
- **Estado del Pipeline:** Consulta el estado del procesamiento de las imágenes en el servidor.
- **Visualización del PDF:** Muestra el reporte PDF generado por el servidor.

### Servidor
- **Recepción y almacenamiento:** Recibe y guarda las imágenes subidas.
- **Preprocesamiento:** Simula el preprocesamiento de las imágenes.
- **Pipeline de Procesamiento:** 
  1. **Evaluación de Calidad:** Verifica la calidad de las imágenes.
  2. **Clasificación RD:** Clasifica las imágenes según la presencia de Retinopatía Diabética.
  3. **Graduación RD:** Asigna un grado a las imágenes que presentan RD.
- **Generación de Reporte:** Crea un reporte en PDF con los resultados.
- **Gestión Asíncrona:** Utiliza Celery para manejar las tareas de forma asíncrona.
- **Consultas de Estado:** Permite consultar el estado del pipeline y recuperar el reporte PDF.

## Tecnologías Utilizadas

- **Cliente:** React, Vite, Tailwind CSS.
- **Backend:** Python 3.10, FastAPI, Celery, Redis, ReportLab.
- **Pruebas:** PyTest.
- **Contenedores:** Docker y Docker Compose.

## Estructura del Proyecto



## Ejecución del Proyecto

### Requisitos Previos
- Docker
- Docker Compose

### Pasos para Ejecutar

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_del_repositorio>
   cd proyecto
   ```

2. **Contruir y levantar los contenedores

```
docker-compose up --build
```

