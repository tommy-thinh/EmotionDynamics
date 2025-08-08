import os
import re
import pandas as pd
from collections import Counter

def count_token_frequencies(textPath, lexPath, savePath):
    # Read the lexicon
    lexicon_df = pd.read_csv(lexPath)
    lexicon_phrases = set(lexicon_df['word'].str.lower())
    emotion_columns = [col for col in lexicon_df.columns if col != 'word']  # Extract emotion columns

    # Read the input text file
    with open(textPath, 'r', encoding='utf-8') as file:
        text = file.read()

    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text.lower())

    # Sliding window algorithm to match phrases in the lexicon
    token_counts = Counter()
    max_phrase_length = max(len(phrase.split()) for phrase in lexicon_phrases)  # Max words in a phrase

    for window_size in range(1, max_phrase_length + 1):  # Sliding window sizes
        for i in range(len(words) - window_size + 1):
            phrase = ' '.join(words[i:i + window_size])  # Create phrase from window
            if phrase in lexicon_phrases:
                token_counts[phrase] += 1

    # Create aggregate CSV file
    os.makedirs(savePath, exist_ok=True)
    aggregate_data = []
    emotion_totals = Counter()

    for phrase, frequency in token_counts.items():
        if phrase in lexicon_df['word'].values:
            for emotion in emotion_columns:
                # Check if the phrase belongs to the emotion (binary value in lexicon)
                emotion_value = lexicon_df.loc[lexicon_df['word'] == phrase, emotion].values[0]
                if emotion_value == 1:
                    aggregate_data.append({'phrase': phrase, 'emotion': emotion, 'frequency': frequency})
                    emotion_totals[emotion] += frequency

    # Save aggregate file
    aggregate_df = pd.DataFrame(aggregate_data)
    aggregate_file = os.path.join(savePath, 'aggregate_frequencies.csv')
    aggregate_df.to_csv(aggregate_file, index=False, encoding='utf-8-sig')
    print(f"Aggregate frequencies saved to {aggregate_file}")

    # Save emotion totals file
    emotion_totals_df = pd.DataFrame(emotion_totals.items(), columns=['emotion', 'frequency'])

    # Sort by frequency in descending order
    emotion_totals_df = emotion_totals_df.sort_values(by='frequency', ascending=False)

    emotion_totals_file = os.path.join(savePath, 'emotion_totals.csv')
    emotion_totals_df.to_csv(emotion_totals_file, index=False, encoding='utf-8-sig')
    print(f"Emotion totals saved to {emotion_totals_file}")

if __name__ == '__main__':
    # Get the directory of the current Python file
    base_dir = os.path.dirname(__file__)

    # Relative paths based on the script's directory
    textPath = os.path.join(base_dir, 'input', 'input.txt')  # Relative path to input text file
    lexPath = os.path.join(base_dir, 'lexicons', 'Vietnamese-NRC-EmoLex.csv')  # Path to lexicon file
    savePath = os.path.join(base_dir, 'output')  # Relative path to save output CSV files

    count_token_frequencies(textPath, lexPath, savePath)