import json
from collections import Counter
from typing import List, Tuple
import zipfile
from memory_profiler import profile
import re

def extract_mentions(text: str) -> List[str]:
    # Search for mentions in the text using regex
    return re.findall(r'@\w+', text)

@profile
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Extracts the top 10 most common user mentions from a JSON file contained within a zip archive,
    while optimizing memory usage by processing the file in batches.

    This function opens the zip file located at `file_path`, extracts the first file within the archive, 
    reads the JSON lines representing tweets, and extracts user mentions from the tweet content. The data 
    is processed in batches using a buffer to minimize memory consumption. The function then counts the 
    frequency of mentions and returns the 10 most common ones.

    Memory profiling is applied to measure memory usage during the function execution.

    Args:
        file_path (str): The path to the zip file containing JSON formatted tweet data.
    
    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains a mention and its count, 
        representing the 10 most common mentions in the data.
    """
    mention_counter = Counter()
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            buffer = []
            for line in f:
                tweet = json.loads(line)
                buffer.append(tweet.get('content', ''))
                
                if len(buffer) >= 1000:
                    for tweet_text in buffer:
                        mentions = extract_mentions(tweet_text)
                        mention_counter.update(mentions)
                    buffer.clear()
            
            for tweet_text in buffer:
                mentions = extract_mentions(tweet_text)
                mention_counter.update(mentions)
    
    return mention_counter.most_common(10)
