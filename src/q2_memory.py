import json
import re
from collections import Counter
from typing import List, Tuple
import zipfile
import emoji
from memory_profiler import profile

def extract_emojis(text: str) -> List[str]:
    return [char for char in text if char in emoji.EMOJI_DATA]


@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counter = Counter()
    
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            buffer = []
            for line in f:
                tweet = json.loads(line)
                buffer.append(tweet.get('content', ''))
                # Processes the buffer when it reaches a suitable size
                if len(buffer) >= 1000:
                    for tweet_text in buffer:
                        emojis = extract_emojis(tweet_text)
                        emoji_counter.update(emojis)
                    buffer.clear()
            
            # Process any remaining tweets in the buffer
            for tweet_text in buffer:
                emojis = extract_emojis(tweet_text)
                emoji_counter.update(emojis)
    
    return emoji_counter.most_common(10)
