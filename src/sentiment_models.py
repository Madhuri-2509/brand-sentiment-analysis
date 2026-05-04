import pandas as pd
import tqdm
import os
from sentiment_models import BERTAnalyzer

# 1. Initialize Model
# This will use the nlptown/bert-base-multilingual-uncased-sentiment model
bert_model = BERTAnalyzer()

# 2. Configuration for Full Dataset
# Using chunks to avoid memory errors and allow for checkpoints
chunk_size = 2000  
output_file = 'data/processed/full_bert_results.csv'
checkpoint_file = 'data/processed/bert_progress_checkpoint.csv'

# Ensure the directory exists
os.makedirs('data/processed', exist_ok=True)

all_texts = df['clean_text'].fillna("").tolist()
bert_sentiments = []

print(f"🎬 Starting processing for {len(all_texts)} reviews.")
print(f"📦 Progress will be saved to {checkpoint_file} every {chunk_size} reviews.")

# 3. Processing Loop
for i in tqdm.tqdm(range(0, len(all_texts), chunk_size)):
    batch_texts = all_texts[i : i + chunk_size]
    
    # Analyze the batch
    batch_results = bert_model.analyze_batch(batch_texts, batch_size=16)
    bert_sentiments.extend(batch_results)
    
    # Save a checkpoint every chunk
    # This stores the current progress so you can recover if it crashes
    checkpoint_df = pd.DataFrame({
        'index': range(0, len(bert_sentiments)),
        'bert_sentiment': bert_sentiments
    })
    checkpoint_df.to_csv(checkpoint_file, index=False)

# 4. Final Integration
# Check if the lengths match before joining
if len(bert_sentiments) == len(df):
    df['bert_sentiment'] = bert_sentiments
    df.to_csv(output_file, index=False)
    print(f"✅ COMPLETE! Full dataset saved to {output_file}")
else:
    print(f"⚠️ Warning: Length mismatch. {len(bert_sentiments)} results vs {len(df)} rows.")