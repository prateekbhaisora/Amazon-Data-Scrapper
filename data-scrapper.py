import os
import pandas as pd
from playwright.sync_api import sync_playwright

INPUT_FILE = './input-urls.txt'
OUTPUT_FILE = './output-data.csv'

counter = 1

def fetch_urls():
    urls = []
    with open(INPUT_FILE, 'r') as f:
        urls = [u.strip() for u in f.readlines()]
    return urls

def get_product_data(url):
    global counter
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        print(f"Opening page for URL {counter}...")
        timer_in_ms = 10000
        page.goto(url, timeout=timer_in_ms)

        timer_in_ms = 10000
        page.wait_for_selector("#productTitle", timeout=timer_in_ms)

        def safe_get(selector):
            try:
                return page.locator(selector).first.inner_text().strip()
            except:
                return None
            
        print(f"Fetching Data for URL {counter}...")

        title = safe_get("#productTitle")
        
        price = (
            safe_get("#priceblock_ourprice") or
            safe_get("#priceblock_dealprice") or
            safe_get(".a-price .a-offscreen")
        )

        rating = safe_get("span.a-icon-alt")
        reviews = safe_get("#acrCustomerReviewText")

        browser.close()
        
        fetched_product_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "reviews": reviews
        }
    
        return fetched_product_data
    
def convert_to_dataFrame(fetched_product_data):
    df = pd.DataFrame([fetched_product_data])
    return df

def write_to_csv(df):
    global counter
    
    file_exists = os.path.isfile(OUTPUT_FILE)

    print(f"Writing data to CSV for URL {counter}...")
    df.to_csv(
        OUTPUT_FILE,
        mode='a',           
        header=not file_exists,  
        index=False
    )

def scrap_product_data_into_df():
    global counter
    
    print("Fetching URL(s)...")
    urls = fetch_urls()
    
    for url in urls:
        print(f"Hitting URL {counter}...")
        fetched_product_data = get_product_data(url)
        
        # print(f"\nExtracted Data for URL {counter}:")
        # for k, v in fetched_product_data.items():
        #     print(f"{k}: {v}")

        df = pd.DataFrame()
            
        if fetched_product_data is not None:
            print(f"Converting fetched data to DataFrame for URL {counter}...")
            df = convert_to_dataFrame(fetched_product_data)
        else:
            print(f"Unable to fetch any data from URL {counter}!")
            
        if not df.empty:
            write_to_csv(df)
            
        counter += 1

def main():
    scrap_product_data_into_df()
    
if __name__ == "__main__":
    main()