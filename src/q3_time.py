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
    mention_counter = Counter()
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            for line in f:
                tweet = json.loads(line)
                mentions = extract_mentions(tweet.get('content', ''))
                mention_counter.update(mentions)
    
    return mention_counter.most_common(10)
