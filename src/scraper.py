import undetected_chromedriver as uc
import pandas as pd
import time
import random
import os
from bs4 import BeautifulSoup
import json

def run_deep_dive_scraper():
    output_file = 'data/raw/trustpilot_reviews_total.csv'
    os.makedirs('data/raw', exist_ok=True)
    
    # Your full 30-brand list
    all_target_brands = [
        "apple", "dell", "hp", "lenovo", "asus", "acer", "microsoft", "msi", "razer",
        "samsung", "google", "motorola", "oneplus", "nokia",
        "bose", "logitech", "sonos", "garmin", "fitbit", "sennheiser",
        "canon", "nikon", "fujifilm", "panasonic", "gopro",
        "sony", "lg", "tp-link", "netgear", "seagate"
    ]
    
    # NEW GOAL: 20 Pages per brand
    PAGES_PER_BRAND = 20  
    all_reviews = []

    # Load existing data to avoid pure duplicates
    if os.path.exists(output_file):
        existing_df = pd.read_csv(output_file)
        all_reviews = existing_df.to_dict('records')
        print(f"📂 Loaded {len(all_reviews)} existing reviews.")
    
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run --password-store=basic")
    driver = uc.Chrome(options=options)

    try:
        for brand in all_target_brands:
            # Check how many reviews we ALREADY have for this brand
            brand_df = pd.DataFrame(all_reviews)
            existing_count = 0
            if not brand_df.empty and 'brand' in brand_df.columns:
                existing_count = len(brand_df[brand_df['brand'] == brand])
            
            # If we already have ~400 reviews (20 pages), we can truly skip it
            if existing_count >= 390: 
                print(f"✅ {brand.upper()} already has {existing_count} reviews. Skipping.")
                continue

            print(f"\n🌍 DEEP DIVE: {brand.upper()} (Currently has {existing_count} reviews)")
            
            for page in range(1, PAGES_PER_BRAND + 1):
                url = f"https://www.trustpilot.com/review/www.{brand}.com?page={page}&languages=en"
                driver.get(url)
                
                if page == 1:
                    print(f"⚠️  CAPTCHA WATCH: Check browser for {brand}!")
                    time.sleep(12) 
                
                time.sleep(random.uniform(7, 11))
                
                soup = BeautifulSoup(driver.page_source, 'lxml')
                script_tag = soup.find("script", id="__NEXT_DATA__")
                
                if script_tag:
                    data = json.loads(script_tag.string)
                    reviews_list = data.get('props', {}).get('pageProps', {}).get('reviews', [])
                    
                    if not reviews_list: break
                        
                    for r in reviews_list:
                        # Logic to prevent adding the exact same review text twice
                        new_review = {
                            "brand": brand,
                            "review_text": r.get('text', ''),
                            "rating": r.get('rating', 0),
                            "date": r.get('dates', {}).get('publishedDate', '')
                        }
                        # Simple duplicate check before appending
                        if new_review not in all_reviews:
                            all_reviews.append(new_review)
                    
                    print(f"   📈 {brand} p.{page} | Total Dataset: {len(all_reviews)}")
                    pd.DataFrame(all_reviews).drop_duplicates().to_csv(output_file, index=False)
                else:
                    print(f"⛔ Blocked. solve captcha.")
                    time.sleep(20)

            print(f"☕ Finished brand. Resting...")
            time.sleep(60)

    finally:
        pd.DataFrame(all_reviews).drop_duplicates().to_csv(output_file, index=False)
        driver.quit()

if __name__ == "__main__":
    run_deep_dive_scraper()