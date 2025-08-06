import os
import re
import pandas as pd
from collections import Counter, defaultdict
import unicodedata

def count_emotion_frequencies(textPath, lexPath, savePath):
    # Define the emotion categories based on your CSV files
    emotions = [
        'anger', 'anticipation', 'disgust', 'fear', 'joy', 
        'negative', 'positive', 'sadness', 'surprise', 'trust'
    ]
    
    # Read all emotion lexicons
    emotion_lexicons = {}
    for emotion in emotions:
        lex_file = os.path.join(lexPath, f'NRC_EmoLex_{emotion}.csv')
        if os.path.exists(lex_file):
            # Read CSV assuming format: word,1
            emotion_df = pd.read_csv(lex_file, header=None, names=['word', 'value'])
            emotion_lexicons[emotion] = set(emotion_df['word'].str.lower())
            print(f"Loaded {len(emotion_lexicons[emotion])} words for {emotion}")
        else:
            print(f"Warning: {lex_file} not found")
            emotion_lexicons[emotion] = set()

    # Read the input text file
    with open(textPath, 'r', encoding='utf-8') as file:
        text = file.read()

    # Normalize text to remove accents and diacritics
    normalized_text = ''.join(
        char for char in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(char) != 'Mn'
    )

    # Tokenize the normalized text
    tokens = re.findall(r'\b\w+\b', normalized_text)

    # Count frequencies for each emotion
    emotion_counts = {}
    for emotion in emotions:
        # Count tokens that appear in this emotion's lexicon
        emotion_tokens = [token for token in tokens if token in emotion_lexicons[emotion]]
        emotion_counts[emotion] = Counter(emotion_tokens)

    # Create output directory
    os.makedirs(savePath, exist_ok=True)

    # Save individual emotion files
    for emotion, token_counts in emotion_counts.items():
        if token_counts:  # Only save if there are tokens found
            result_df = pd.DataFrame(token_counts.items(), columns=['token', 'frequency'])
            result_df = result_df.sort_values('frequency', ascending=False)
            
            output_file = os.path.join(savePath, f'{emotion}_token_frequencies.csv')
            result_df.to_csv(output_file, index=False)
            print(f"{emotion}: {len(result_df)} unique tokens, saved to {output_file}")

    # Create a summary file with total counts per emotion
    summary_data = []
    for emotion in emotions:
        total_tokens = sum(emotion_counts[emotion].values())
        unique_tokens = len(emotion_counts[emotion])
        summary_data.append({
            'emotion': emotion,
            'total_token_count': total_tokens,
            'unique_token_count': unique_tokens
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = os.path.join(savePath, '.emotion_summary.csv')
    summary_df.to_csv(summary_file, index=False)
    print(f"Summary saved to {summary_file}")

    # Create a detailed breakdown showing which emotions each token belongs to
    token_emotion_map = defaultdict(list)
    for emotion, token_counts in emotion_counts.items():
        for token in token_counts:
            token_emotion_map[token].append({
                'emotion': emotion,
                'frequency': token_counts[token]
            })
    
    # Convert to DataFrame for detailed analysis
    detailed_data = []
    for token, emotion_list in token_emotion_map.items():
        for emotion_info in emotion_list:
            detailed_data.append({
                'token': token,
                'emotion': emotion_info['emotion'],
                'frequency': emotion_info['frequency']
            })
    
    if detailed_data:
        detailed_df = pd.DataFrame(detailed_data)
        detailed_file = os.path.join(savePath, 'token_emotion_breakdown.csv')
        detailed_df.to_csv(detailed_file, index=False)
        print(f"Detailed token-emotion breakdown saved to {detailed_file}")

if __name__ == '__main__':
    # Get the directory of the current Python file
    base_dir = os.path.dirname(__file__)

    # Relative paths based on the script's directory
    textPath = os.path.join(base_dir, 'input', 'input.txt')  # Relative path to input text file
    lexPath = os.path.join(base_dir, 'lexicons')  # Path to lexicons folder
    savePath = os.path.join(base_dir, 'output')  # Relative path to save output CSV files

    count_emotion_frequencies(textPath, lexPath, savePath)