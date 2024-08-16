from typing import List, Tuple
from datetime import datetime
from memory_profiler import profile
import zipfile
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc, date_format
from pyspark import StorageLevel
import os
import sys

# The top 10 dates where there are more tweets. Mention the user (username) that 
# has the most posts for each of those days. 

@profile
def q1_memory(zip_file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    It parses a zip file containing tweets in JSONL format, identifies the 10 dates with the most tweets and determines the user with the most tweets for each of those dates. The function also measures memory usage.

    Args: zip_file_path (str): The path to the zip file containing the JSONL file with tweet data.

    Returns: List[Tuple[datetime.date, str]]: A list of tuples, where each tuple contains a date (`datetime.date`) and the name of the user with the most tweets on that date (`str`).


    Process:
        Extract the JSONL file from the zip archive into a temporary directory. 
        Use PySpark to read the JSONL file and select the necessary columns (date and username).        
        Extract the JSONL file from the zip archive into a temporary directory.  
        Use PySpark to read the JSONL file and select the necessary columns (date and username).  
        Group the tweets by date and user, counting the number of tweets. 
        Identify the 10 dates with the most tweets, then find the user who posted the most tweets on each of those dates.
        Clean up the temporary files and the directory used for extraction. 
        Return the list of the 10 dates with the most tweets along with the most active user on each.
    """
    

    spark = SparkSession.builder.appName("q1_memory").getOrCreate()
    temp_dir  ='tmp_file'
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir )

    df = spark.read.json(temp_dir )

    df = df.select(date_format(col("date"), "yyyy-MM-dd").alias("date"), col("user.username").alias("username"))

    df.persist(StorageLevel.DISK_ONLY)

    grouped_df = df.groupBy("date", "username").agg(count("*").alias("tweet_count"))

    result = (grouped_df
              .groupBy("date")
              .agg({"tweet_count": "max"})
              .orderBy(desc("max(tweet_count)"))
              .limit(10))

    top_10_dates = result.collect()

    top_10_with_user : List[Tuple[datetime.date, str]] = []
    for row in top_10_dates:
        date = row['date']
        max_tweets = row['max(tweet_count)']
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        user_row = grouped_df.filter((col("date") == date) & (col("tweet_count") == max_tweets)).select("username").limit(1).collect()[0]
        top_10_with_user.append((date_obj, user_row["username"]))


    
    for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            os.unlink(file_path)
    os.rmdir(temp_dir)
    return top_10_with_user


if __name__ == "__main__":
    zip_file_path = sys.argv[1]
    q1_memory(zip_file_path)