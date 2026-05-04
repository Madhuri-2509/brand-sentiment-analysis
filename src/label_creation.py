import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def run_brand_sentiment_eda():
    input_path = 'data/processed/cleaned_reviews_final.csv'
    output_path = 'data/processed/labeled_reviews.csv'
    plot_dir = 'reports/plots'
    
    if not os.path.exists(input_path):
        print(f"❌ Error: Cleaned file not found. Run cleaning first!")
        return
    if not os.path.exists(plot_dir): 
        os.makedirs(plot_dir)

    # 1. LOAD & LABEL
    print("📂 Loading data and applying labels...")
    df = pd.read_csv(input_path)
    
    def categorize_rating(rating):
        if rating >= 4: return 'Positive'
        elif rating == 3: return 'Neutral'
        else: return 'Negative'

    df['rating_sentiment'] = df['rating'].apply(categorize_rating)
    df.to_csv(output_path, index=False)

    # 2. GENERATE BRAND COMPARISON GRAPH
    print("📊 Generating Brand Sentiment Comparison Graph...")
    
    # Selecting the top 15 brands by review volume for a clean visual
    top_brands = df['brand'].value_counts().head(15).index
    df_top = df[df['brand'].isin(top_brands)]

    # Create a cross-tabulation of Brand vs Sentiment
    brand_comp = pd.crosstab(df_top['brand'], df_top['rating_sentiment'], normalize='index') * 100
    
    # Ensure columns are in the correct order for the legend
    cols = [c for c in ['Positive', 'Neutral', 'Negative'] if c in brand_comp.columns]
    brand_comp = brand_comp[cols]
    
    # Sort by Positive sentiment so the "best" brands appear at the top
    brand_comp = brand_comp.sort_values(by='Positive', ascending=True) 

    # Plotting
    plt.figure(figsize=(12, 10))
    ax = brand_comp.plot(kind='barh', 
                         stacked=True, 
                         figsize=(12, 8),
                         color={'Positive': "#5b2ecc", 'Neutral': '#f1c40f', 'Negative': '#e74c3c'})
    
    plt.title('Brand Sentiment Comparison (Based on User Ratings)', fontsize=15, fontweight='bold')
    plt.xlabel('Percentage of Total Reviews (%)')
    plt.ylabel('Brand')
    plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add a grid for better readability
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'brand_sentiment_comparison.png'), dpi=300)
    plt.close()

    print(f" Success! Graph saved to: {plot_dir}/brand_sentiment_comparison.png")

if __name__ == "__main__":
    run_brand_sentiment_eda()