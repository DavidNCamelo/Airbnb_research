# Airbnb_research

El presente tiene intención informativa, a fin de tener indicios sobre el nivel de uso de la plataforma AIRBNB en la cuidad de Medellin y su área metropolitana. Se tuvieron en cuenta las siguientes variables:

    - Precio.
    - Cantidad de habitaciones.
    - Ubicacion.
    - Fecha de creación
    - Camaras de seguridad en el sitio
    - Calificaciones de los usuarios.

El proyecto contó con las siguientes fases:
1. Extracción de Ids de habitaciones disponibles mediante web scrapping
2. Extracción de información relevante sobre las habitaciones mediante web scrapping
3. Procesamiento y Análisis de datos

Los jupyter notebook contienen la tercera y última fase de un proceso de exploración, extracción, transformación y análisis de datos sobre la oferta de alojamiento presente en la plataforma AirBnb tanto en el Área Metropolitana del Valle de Aburrá como en Medellín Colombia, realizando un análisis más profundo sobre éste último.

En la primera fase del ejercicio se recolectaron 9106 IDs únicos, los cuáles sirvieron para extraer la información requerida, mientras que la segunda fase se logró ingresar a 8792 ids distintos teniendo así una recolección de 96.55% del total de ids de la primera fase. Éste resultado se debió a que la plataforma posiblemente ocultó alguno de los resultados, implicando que al no ser públicos en el momento de ejecutar la segunda fase no fueran encontrados para extraer información deseada. No obstante, aunque se haya recolectado ese alto valor, algunos ids no extrajeron información de los campos deseados. Después de la limpieza a través de title y description que son campos tan importantes como ids, además muestra una cierta cantidad de valores nulos en este caso presenta una proporción de 1.0% sobre del total de datos recolectados durante la segunda fase presentando que la recolección de datos tuvo un éxito considerable, quedando con un total de 8192 alojamientos únicos en toda la zona Metropolitana del Valle de Aburrá.

Para claridad el Valle de Aburrá está compuesto de la siguiente manera:
![image](https://github.com/DavidNCamelo/Airbnb_research/assets/93718360/273bb6b3-82aa-467c-99a8-7c7ba5251385)
