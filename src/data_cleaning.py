import pandas as pd
import os

def clean_all_data():
    # 1. SETUP PATHS
    tp_path = 'data/raw/trustpilot_reviews_total.csv'
    amz_path = 'data/processed/amazon_filtered.csv'
    output_path = 'data/processed/cleaned_reviews_final.csv'
    
    print("Starting Unified Data Cleaning (Trustpilot + Amazon)...")

    # 2. LOAD DATASETS
    # We use low_memory=False to handle the mixed types we saw earlier
    df_tp = pd.read_csv(tp_path, low_memory=False)
    df_amz = pd.read_csv(amz_path, low_memory=False)

    # 3. STANDARDIZE COLUMNS
    # Trustpilot Cleanup
    df_tp['source'] = 'Trustpilot'
    df_tp['period'] = 'Present'
    
    # Amazon Cleanup
    df_amz['source'] = 'Amazon'
    df_amz['period'] = 'Past'

    # 4. THE CLEANING FUNCTION
    def clean_df(df):
        # Force numeric ratings and keep only 1-5
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[df['rating'].between(1, 5)].copy()
        
        # Remove null or empty reviews
        df = df.dropna(subset=['review_text'])
        df = df[df['review_text'].str.strip() != ""].copy()
        
        # Standardize Brand Names
        df['brand'] = df['brand'].astype(str).str.lower().str.strip()
        
        # Remove exact duplicate reviews within the same brand
        df = df.drop_duplicates(subset=['brand', 'review_text'])
        return df

    print(" Cleaning Trustpilot data...")
    df_tp_clean = clean_df(df_tp)
    
    print(" Cleaning Amazon data...")
    df_amz_clean = clean_df(df_amz)

    # 5. MERGE & SAVE
    df_final = pd.concat([df_tp_clean, df_amz_clean], ignore_index=True)
    
    os.makedirs('data/processed', exist_ok=True)
    df_final.to_csv(output_path, index=False)

    print("\n" + "="*35)
    print(f"UNIFIED CLEANING COMPLETE")
    print("="*35)
    print(f"Trustpilot Cleaned: {len(df_tp_clean)} rows")
    print(f"Amazon Cleaned:     {len(df_amz_clean)} rows")
    print(f"Combined Total:     {len(df_final)} rows")
    print(f"File Saved to:      {output_path}")

if __name__ == "__main__":
    clean_all_data()