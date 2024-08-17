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
    mention_counter = Counter()
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            buffer = []
            for line in f:
                tweet = json.loads(line)
                buffer.append(tweet.get('content', ''))
                
                # Procesa el buffer cuando llega a un tamaño adecuado
                if len(buffer) >= 1000:
                    for tweet_text in buffer:
                        mentions = extract_mentions(tweet_text)
                        mention_counter.update(mentions)
                    buffer.clear()
            
            # Procesar cualquier tweet restante en el buffer
            for tweet_text in buffer:
                mentions = extract_mentions(tweet_text)
                mention_counter.update(mentions)
    
    return mention_counter.most_common(10)
