import os
import re
import pandas as pd
from collections import Counter
import unicodedata

def count_token_frequencies(textPath, lexPath, savePath):
    # Read the lexicon
    lexicon_df = pd.read_csv(lexPath)
    lexicon_words = set(lexicon_df['word'].str.lower())

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

    # Count frequencies of tokens found in the lexicon
    token_counts = Counter(token for token in tokens if token in lexicon_words)

    # Convert to DataFrame
    result_df = pd.DataFrame(token_counts.items(), columns=['token', 'frequency'])

    # Save to CSV
    os.makedirs(savePath, exist_ok=True)
    output_file = os.path.join(savePath, 'token_frequencies.csv')
    result_df.to_csv(output_file, index=False)
    print(f"Token frequencies saved to {output_file}")

if __name__ == '__main__':
    # Get the directory of the current Python file
    base_dir = os.path.dirname(__file__)

    # Relative paths based on the script's directory
    textPath = os.path.join(base_dir, 'input', 'input.txt')  # Relative path to input text file
    lexPath = os.path.join(base_dir, 'lexicons', 'NRC-VAD-Lexicon-v2.1.csv')  # Relative path to lexicon file
    savePath = os.path.join(base_dir, 'output')  # Relative path to save output CSV file

    count_token_frequencies(textPath, lexPath, savePath)