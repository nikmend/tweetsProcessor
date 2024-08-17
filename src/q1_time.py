import json
import pandas as pd
from multiprocessing import Pool
from datetime import datetime
import zipfile
from typing import List, Tuple

def process_chunk(chunk):
    # Procesa un chunk de datos JSON
    data = [json.loads(line) for line in chunk]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df[['date', 'user']].groupby(['date', 'user']).size().reset_index(name='counts')

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Abrir el archivo JSONL
    with open(file_path, 'rb') as zip_file:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            jsonl_file_name = [f for f in zip_ref.namelist() if f.endswith('.json')][0]

            print('# Leer el archivo JSONL en memoria con utf-8 encoding')
            with zip_ref.open(jsonl_file_name) as jsonl_file:
                lines = jsonl_file.read().decode('utf-8').splitlines()

                print('# Dividir el archivo en chunks para paralelización')
                chunk_size = len(lines) // 4  # Procesar en 4 núcleos
                chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

                print('# Procesar los chunks en paralelo')
                with Pool(4) as pool:
                    results = pool.map(process_chunk, chunks)

                print('# Combinar resultados')
                df_combined = pd.concat(results)

                print('# Obtener top 10 fechas con más tweets y el usuario con más tweets')
                top_10_dates = df_combined.groupby('date')['counts'].sum().nlargest(10)

                result = []
                for date in top_10_dates.index:
                    max_user = df_combined[df_combined['date'] == date].groupby('user')['counts'].sum().idxmax()
                    result.append((date, max_user))

                return result
