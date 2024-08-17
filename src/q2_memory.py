import json
import re
from collections import Counter
from typing import List, Tuple
import zipfile
import emoji
from memory_profiler import profile

def extract_emojis(text: str) -> List[str]:
    #Extracts emojis from a given text using the emoji library.
    return [char for char in text if char in emoji.EMOJI_DATA]


@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Extracts the top 10 most common emojis from a JSON file contained within a zip archive,
    while optimizing memory usage by processing the file in batches.

    This function opens the zip file located at `file_path`, extracts the first file within the archive, 
    reads the JSON lines representing tweets, and extracts emojis from the tweet content. The data is 
    processed in batches using a buffer to minimize memory consumption. The function then counts the 
    frequency of emojis and returns the 10 most common ones.

    Memory profiling is applied to measure memory usage during the function execution.

    Args:
        file_path (str): The path to the zip file containing JSON formatted tweet data.
    
    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains an emoji and its count, 
        representing the 10 most common emojis in the data.
    """
    
    emoji_counter = Counter()
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            buffer = []
            for line in f:
                tweet = json.loads(line)
                buffer.append(tweet.get('content', ''))
                if len(buffer) >= 1000:
                    for tweet_text in buffer:
                        emojis = extract_emojis(tweet_text)
                        emoji_counter.update(emojis)
                    buffer.clear()
            
            for tweet_text in buffer:
                emojis = extract_emojis(tweet_text)
                emoji_counter.update(emojis)
    
    return emoji_counter.most_common(10)
