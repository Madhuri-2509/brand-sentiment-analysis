import pandas as pd
import os

def clean_and_merge():
    tp_raw = 'data/raw/trustpilot_reviews_total.csv'
    amz_raw = 'data/processed/amazon_filtered.csv'
    output_path = 'data/processed/cleaned_reviews_final.csv'
    
    print(" Starting final unified cleaning...")

    # Load data
    df_tp = pd.read_csv(tp_raw, low_memory=False)
    df_amz = pd.read_csv(amz_raw, low_memory=False)

    def clean_dataset(df, source_name, period_name):
        # 1. Flexible Column Mapping
        # If your Trustpilot file uses 'reviewText' instead of 'review_text', this fixes it
        if 'reviewText' in df.columns and 'review_text' not in df.columns:
            df = df.rename(columns={'reviewText': 'review_text'})
        if 'overall' in df.columns and 'rating' not in df.columns:
            df = df.rename(columns={'overall': 'rating'})

        # 2. Convert and Filter Ratings
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[df['rating'].between(1, 5)].copy()
        
        # 3. Clean Text
        df['review_text'] = df['review_text'].fillna('').astype(str)
        df = df[df['review_text'].str.strip() != ""].copy()
        
        # 4. Standardize Brands
        df['brand'] = df['brand'].astype(str).str.lower().str.strip()
        
        # 5. Metadata
        df['source'] = source_name
        df['period'] = period_name
        
        # 6. Deduplicate
        return df.drop_duplicates(subset=['brand', 'review_text'])

    # Execute
    print(" Cleaning Trustpilot...")
    df_tp_clean = clean_dataset(df_tp, 'Trustpilot', 'Present')
    
    print(" Cleaning Amazon...")
    df_amz_clean = clean_dataset(df_amz, 'Amazon', 'Past')

    # Merge
    df_final = pd.concat([df_tp_clean, df_amz_clean], ignore_index=True)
    
    os.makedirs('data/processed', exist_ok=True)
    df_final.to_csv(output_path, index=False)

    print("\n" + "="*35)
    print(f"CLEANING RESULTS")
    print("="*35)
    print(f"Trustpilot (Present): {len(df_tp_clean)} rows")
    print(f"Amazon (Past):      {len(df_amz_clean)} rows")
    print(f"Final Combined:     {len(df_final)} rows")

if __name__ == "__main__":
    clean_and_merge()