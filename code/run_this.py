import os
import re
import pandas as pd
from collections import Counter
import sys
from argparse import ArgumentParser
import unicodedata

parser = ArgumentParser()
parser.add_argument('--textPath', help='path to input text file', required=True)
parser.add_argument('--lexPath', help='path to lexicon file (single column with words)', required=True)
parser.add_argument('--savePath', help='path to save output CSV file', required=True)

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
    args = parser.parse_args()
    count_token_frequencies(args.textPath, args.lexPath, args.savePath)