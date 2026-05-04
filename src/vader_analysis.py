import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure VADER is ready
nltk.download('vader_lexicon')

def run_common_brand_vader():
    input_path = 'data/processed/preprocessed_reviews.csv'
    output_dir = 'reports/plots'
    
    if not os.path.exists(input_path):
        print("❌ Error: Run preprocessing first!")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. LOAD DATA
    df = pd.read_csv(input_path)
    
    # 2. IDENTIFY COMMON BRANDS
    # Get set of brands in Past and set of brands in Present
    past_brands = set(df[df['period'] == 'Past']['brand'].unique())
    present_brands = set(df[df['period'] == 'Present']['brand'].unique())
    
    # Find the intersection (brands in both)
    common_brands = list(past_brands.intersection(present_brands))
    
    print(f"🔍 Found {len(common_brands)} brands present in both datasets.")
    print(f"Brands: {', '.join(common_brands)}")

    # 3. FILTER DATASET
    df_filtered = df[df['brand'].isin(common_brands)].copy()

    # 4. RUN VADER SCORING
    print("🧠 Scoring common brands with VADER...")
    analyzer = SentimentIntensityAnalyzer()
    df_filtered['vader_score'] = df_filtered['review_text'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])

    # 5. CREATE TREND TABLE
    trend_table = df_filtered.groupby(['brand', 'period'])['vader_score'].mean().unstack()
    # Reorder columns to ensure 'Past' is first
    trend_table = trend_table[['Past', 'Present']]
    
    print("\n📈 LONGITUDINAL TREND TABLE:")
    print(trend_table.round(3))

    # 6. VISUALIZE THE SHIFT
    plt.figure(figsize=(12, 8))
    trend_table_sorted = trend_table.sort_values(by='Past', ascending=False)
    
    trend_table_sorted.plot(kind='bar', figsize=(14, 7), color=['#3498db', '#e74c3c'])
    
    plt.title('Sentiment Evolution of Common Brands: Amazon vs Trustpilot', fontsize=15, fontweight='bold')
    plt.ylabel('Average VADER Score (-1 to 1)')
    plt.xlabel('Brand')
    plt.legend(title='Period')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=1) # Baseline
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'common_brand_evolution.png'), dpi=300)
    
    print(f"\n✅ Analysis complete! Graph saved to {output_dir}/common_brand_evolution.png")

if __name__ == "__main__":
    run_common_brand_vader()