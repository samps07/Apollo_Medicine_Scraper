import requests
import csv
import time
from bs4 import BeautifulSoup #required for coverting raw html content to searchable format

# URL from network tab of Apollo website
url = "https://search.apollo247.com/v3/fullSearch"

# Headers from website to ensure access
Headers = { 
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.apollopharmacy.in",
    "referer": "https://www.apollopharmacy.in/",
    "authorization": "Oeu324WMvfKOj5KMJh2Lkf00eW1",
    "user-agent": "Mozilla/5.0"
}

all_Medicines = []
search_term = "paracetamol"
pincode = "560064"
page = 1

def scrape_product_details(product_url):
    product_details = {}

    try:
        response = requests.get(product_url, headers=Headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser') #converts the webpage’s HTML content (response.text) into a format that’s easy to search using BeautifulSoup, storing it in soup.

            # About Section
            about_section = soup.find("div", id="About Product Web") #finds html data from soup corresponding to tag and id, extracted from page source
            product_details["About"] = (
                about_section.find("div", class_="Yh").get_text(strip=True) 
                if about_section and about_section.find("div", class_="Yh") else "N/A"
            )

            # Uses Section
            uses_section = soup.find("div", id="Uses Web")
            product_details["Uses"] = (
                uses_section.find("div", class_="Yh").get_text(strip=True) 
                if uses_section and uses_section.find("div", class_="Yh") else "N/A"
            )

            # Directions for Use
            directions_section = soup.find("div", id="Directions for use Web")
            product_details["DirectionsForUse"] = (
                directions_section.find("div", class_="Yh").get_text(strip=True) 
                if directions_section and directions_section.find("div", class_="Yh") else "N/A"
            )

            # Medicinal Benefits
            benefits_section = soup.find("div", id="Medicinal Benefits Web")
            product_details["MedicinalBenefits"] = (
                benefits_section.find("div", class_="Yh").get_text(strip=True) 
                if benefits_section and benefits_section.find("div", class_="Yh") else "N/A"
            )

            # How Drug Works
            how_works_section = soup.find("div", id="How Drug Works Web")
            product_details["HowItWorks"] = (
                how_works_section.find("div", class_="Yh").get_text(strip=True) 
                if how_works_section and how_works_section.find("div", class_="Yh") else "N/A"
            )

            # Images Section
            carousel_slides = soup.find_all("div", class_="keen-slider__slide")
            image_urls = []
            for slide in carousel_slides:
                img = slide.find("img", class_="bD")
                if img and img.get("src"):
                    # Optionally strip query parameters for cleaner URLs
                    image_urls.append(img["src"].split("?")[0]) #If the image exists and has a src attribute (the URL), takes the URL, removes any query parameters and adds it to image_urls.
            
            product_details["Images"] = ", ".join(image_urls) if image_urls else "N/A"

        else:
            print(f"Failed to fetch {product_url}: Status code {response.status_code}")

    except Exception as e:
        print(f"Error fetching details from {product_url}: {e}")

    return product_details

while len(all_Medicines) < 70:
    payload = {
        "query": search_term,
        "page": page,
        "productsPerPage": 24,
        "selSortBy": "relevance",
        "pincode": pincode,
        "filters": []
    }
    try:
        fetched_data = requests.post(url, headers=Headers, json=payload)
        fetched_data_json = fetched_data.json()

        if "data" not in fetched_data_json or "products" not in fetched_data_json["data"]:
            print("No more products found or API error")
            break

        for product in fetched_data_json["data"]["products"]:
            status = product.get("status", "").lower()
            if status == "out-of-stock":
                continue

            med = {
                "Name": product.get("name", ""),
                "MRP": product.get("price", ""),
                "SellingPrice": product.get("specialPrice", ""),
                "Tags": product.get("tags", ""),
                "product_id": product.get("id", ""),
                "SKU": product.get("sku", ""),
                "product_link": f'https://www.apollopharmacy.in/otc/{product.get("urlKey", "")}?doNotTrack=true'
            }

            product_details = scrape_product_details(med["product_link"])
            med.update(product_details) #adding product details from product page
            all_Medicines.append(med)

            if len(all_Medicines) >= 70:
                break

    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        break

    page += 1
    time.sleep(2)  # Increased to avoid rate limiting

if all_Medicines:
    keys = all_Medicines[0].keys()
    with open("scraped_medicines_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_Medicines)

print("Done! Saved 70 in-stock medicine details to scraped_medicines_data.csv")
