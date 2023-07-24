import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape a single product page
def scrape_product_page(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    webpage = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extracting product details
    product_name = soup.find("span", attrs={'id': 'productTitle'})
    product_price = soup.find("span", attrs={'id': 'priceblock_ourprice'})
    product_rating = soup.find("span", attrs={'class': 'a-icon-alt'})
    num_reviews = soup.find("span", attrs={'id': 'acrCustomerReviewText'})
    asin = soup.find("input", attrs={'id': 'ASIN'})
    product_description = soup.find("meta", attrs={'name': 'title'})
    manufacturer = soup.find("a", attrs={'id': 'bylineInfo'})

    # Handling cases where elements are not found
    product_name = product_name.text.strip() if product_name else "N/A"
    product_price = product_price.text.strip() if product_price else "N/A"
    product_rating = product_rating.text.strip().split()[0] if product_rating else "N/A"
    num_reviews = num_reviews.text.strip() if num_reviews else "N/A"
    asin = asin['value'].strip() if asin else "N/A"
    product_description = product_description['content'].strip() if product_description else "N/A"
    manufacturer = manufacturer.text.strip() if manufacturer else "N/A"

    return {
        'Product URL': product_url,
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating': product_rating,
        'Number of Reviews': num_reviews,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

# Main function to scrape multiple product listing pages
def scrape_product_listings(base_url, num_pages):
    data = []
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}&page={page_num}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Extracting product links
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        for link in links:
            product_url = "https://www.amazon.in/" + link['href']
            product_data = scrape_product_page(product_url)
            data.append(product_data)

    return data

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
    num_pages_to_scrape = 20

    # Scrape the data from the product listing pages
    scraped_data = scrape_product_listings(base_url, num_pages_to_scrape)

    # Create a DataFrame and save it to a CSV file
    df = pd.DataFrame(scraped_data)
    df.to_csv('product_data.csv', index=False)

    print("Scraping and saving to CSV completed successfully.")
