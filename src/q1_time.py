import json
from collections import defaultdict, Counter
from typing import List, Tuple
import zipfile
import datetime
from memory_profiler import profile

@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Analyzes tweet data from a JSON file contained within a zip archive to identify the 
    most active user for the top 10 dates with the highest tweet counts.

    This function decompresses a zip file containing JSON formatted tweet data, processes 
    each tweet to count the number of tweets per user for each date, and then identifies 
    the top 10 dates with the most tweets. For each of these dates, it returns the user 
    who tweeted the most on that day.

    Memory profiling is applied to measure memory usage during the function execution.

    Args:
        file_path (str): The path to the zip file containing JSON formatted tweet data.
    
    Returns:
        List[Tuple[datetime.date, str]]: A list of tuples where each tuple contains a date 
        and the username of the most active user for that date, limited to the top 10 most active days.
    """
    date_user_counter = defaultdict(Counter)
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            for line in f:
                tweet = json.loads(line)
                date = tweet.get('date')
                username = tweet.get('user', {}).get('username')
                if date and username:
                    date = datetime.datetime.fromisoformat(date).date()
                    date_user_counter[date].update([username])
    
    # Encontramos las 10 fechas con más tweets
    top_dates = sorted(date_user_counter.keys(), key=lambda d: sum(date_user_counter[d].values()), reverse=True)[:10]
    
    # Para cada fecha, encontramos el usuario con más publicaciones
    result = [(date, date_user_counter[date].most_common(1)[0][0]) for date in top_dates]
    
    return result
