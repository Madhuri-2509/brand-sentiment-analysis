import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os

# Download required NLTK assets
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

def advanced_preprocess(text):
    # 1. Lowercase & String conversion
    text = str(text).lower()
    
    # 2. Remove URLs and Special Characters
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Stopword Removal & Lemmatization
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Keep words only if they aren't stopwords and are longer than 2 letters
    clean_tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and len(w) > 2]
    
    return " ".join(clean_tokens)

def run_preprocessing():
    input_path = 'data/processed/labeled_reviews.csv'
    output_path = 'data/processed/preprocessed_reviews.csv'
    
    if not os.path.exists(input_path):
        print(f" Error: Labeled file not found at {input_path}")
        return

    print("Loading data for NLP Preprocessing...")
    df = pd.read_csv(input_path)

    print(f"Processing {len(df)} reviews. This may take 2-3 minutes...")
    
    # Applying the advanced cleaning
    df['clean_text'] = df['review_text'].apply(advanced_preprocess)

    # Save the result
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*40)
    print(" PREPROCESSING & LEMMATIZATION COMPLETE")
    print("="*40)
    print(f"Original: {df['review_text'].iloc[0][:60]}...")
    print(f"Cleaned:  {df['clean_text'].iloc[0][:60]}...")

if __name__ == "__main__":
    run_preprocessing()