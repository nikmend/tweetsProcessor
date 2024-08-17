import json
from collections import Counter
from typing import List, Tuple
import zipfile
import re

from memory_profiler import profile


def extract_mentions(text: str) -> List[str]:
    # Search for mentions in the text using regex
    return re.findall(r'@\w+', text)

@profile
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Extracts the top 10 most common user mentions from a JSON file contained within a zip archive.
    
    This function opens the zip file located at `file_path`, extracts the first file within the archive, 
    reads the JSON lines representing tweets, and extracts user mentions from the tweet content. 
    It then counts the frequency of mentions and returns the 10 most common ones.

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
            for line in f:
                tweet = json.loads(line)
                mentions = extract_mentions(tweet.get('content', ''))
                mention_counter.update(mentions)
    
    return mention_counter.most_common(10)
