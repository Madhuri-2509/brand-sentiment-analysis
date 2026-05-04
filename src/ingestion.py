import pandas as pd
import os

def integrate_amazon_data():
    # Using the exact path you provided
    amazon_file_path = r"C:\Users\madhu\brand-perception-analysis\brand-perception-analysis\data\processed_reviews_with_brands.csv" 
    
    output_path = 'data/processed/amazon_filtered.csv'
    
    # Ensuring we focus on the brands consistent with your Trustpilot scrape
    target_brands = [
        "apple", "sony", "samsung", "dell", "hp", "lenovo", "asus", 
        "microsoft", "logitech", "canon", "nikon", "msi", "razer"
    ]

    if not os.path.exists(amazon_file_path):
        print(f"❌ ERROR: File not found at {amazon_file_path}")
        return

    print(f"🚀 Found file! Integrating Amazon historical data...")

    try:
        # Load the Amazon dataset
        df_old = pd.read_csv(amazon_file_path)
        
        # Standardize the brand column
        if 'brand' in df_old.columns:
            df_old['brand'] = df_old['brand'].astype(str).str.lower()
        else:
            print("❌ 'brand' column missing in the old file. Check column names!")
            return

        # Filter for our 30-brand scope
        df_filtered = df_old[df_old['brand'].isin(target_brands)].copy()

        # Map to our standard format: brand, review_text, rating, source, period
        # Note: Adjust 'review_text' or 'rating' if your old file used different names like 'reviewText'
        df_final = pd.DataFrame({
            'brand': df_filtered['brand'],
            'review_text': df_filtered.get('review_text', df_filtered.get('reviewText', '')),
            'rating': df_filtered.get('rating', df_filtered.get('overall', 0)),
            'source': 'Amazon_Historical',
            'period': 'Past'
        })

        # Save to your current project folder
        os.makedirs('data/processed', exist_ok=True)
        df_final.to_csv(output_path, index=False)
        
        print(f"✅ SUCCESS! Extracted {len(df_final)} reviews.")
        print(f"📍 Saved to: {output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    integrate_amazon_data()