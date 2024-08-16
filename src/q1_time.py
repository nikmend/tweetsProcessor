

from typing import List, Tuple
from datetime import datetime
from memory_profiler import profile
import zipfile
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc, date_format
from pyspark import StorageLevel
import os


# The top 10 dates where there are more tweets. Mention the user (username) that 
# has the most posts for each of those days. 

@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """    """
    spark = SparkSession.builder.appName("q1_time").getOrCreate()


    with open(file_path, 'rb') as zip_file:
        zip_file.name
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Leer el archivo JSONL en memoria sin extraerlo
            with zip_ref.open(zip_ref.filelist[0].filename) as jsonl_file:
  
                json_bytes = jsonl_file.read().decode("utf-8")
                    
                # Crear un DataFrame directamente desde el JSONL cargado en memoria
                df = spark.read.json(spark.sparkContext.parallelize([json_bytes]))

                # Seleccionar las columnas necesarias y formatear la fecha
                df = df.select(date_format(col("date"), "yyyy-MM-dd").alias("date"), col("user.username").alias("username"))

                # Almacenar los datos en memoria para optimizar el tiempo
                df.cache()

                # Contar tweets por fecha y usuario y obtener las top 10 fechas con más tweets
                result = (df.groupBy("date", "username")
                            .agg(count("*").alias("tweet_count"))
                            .groupBy("date")
                            .agg({"tweet_count": "max"})
                            .orderBy(desc("max(tweet_count)"))
                            .limit(10))

                # Obtener el usuario con más tweets en cada una de las top 10 fechas
                top_10_dates = result.collect()

                # Recoger la lista de fechas con el usuario que más tweets tiene en cada una de esas fechas
                top_10_with_user: List[Tuple[datetime.date, str]] = []
                for row in top_10_dates:
                    date_str = row['date']
                    max_tweets = row['max(tweet_count)']

                    # Convertir la fecha a datetime.date
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                    # Filtrar para obtener el usuario con más tweets en esa fecha
                    user_row = df.filter((col("date") == date_str) & (col("tweet_count") == max_tweets)).select("username").limit(1).collect()[0]
                    top_10_with_user.append((date_obj, user_row["username"]))

                # Devolver el resultado final en el formato requerido
                return top_10_with_user