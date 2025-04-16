import requests
import csv
import time

#url found from network tab of apollo website
url="https://search.apollo247.com/v3/fullSearch"

#headers from website to ensure access
Headers={ 
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.apollopharmacy.in",
    "referer": "https://www.apollopharmacy.in/",
    "authorization": "Oeu324WMvfKOj5KMJh2Lkf00eW1",
    "user-agent": "Mozilla/5.0"
    }

all_Medicines=[] #empty list to hold scraped medicines data
search_term="paracetamol" #assumed generic medicine
pincode="560064" #assumed pincode
page=1 #initial page

while len(all_Medicines)<70:
    payload = {
        "query": search_term,
        "page": page,
        "productsPerPage": 24,
        "selSortBy": "relevance",
        "pincode": pincode,
        "filters": []
    }
    fetched_data = requests.post(url, headers=Headers, json=payload) #POST request
    fetched_data_json=fetched_data.json() #converting into JSON
    #SAFETY CHECK
    if "data" not in fetched_data_json or "products" not in fetched_data_json["data"]:
        break
    for product in fetched_data_json["data"]["products"]:
        #filtering out-of-stock products
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
        
        all_Medicines.append(med)#adding scraped data in form of dictionay one by one
        
        if len(all_Medicines)>70:
            break
    page+=1 #if 70 not found in the first page
    time.sleep(1.5) #time delay to respect apollo server

# Save scraped data to a CSV file
if all_Medicines:
    keys = all_Medicines[0].keys()
    with open("scraped_medicines_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys) #write dictionaries from medicines into f
        writer.writeheader() #write keys as headers into f
        writer.writerows(all_Medicines) #write scraped data into f

print("Done! Saved 70 in-stock medicine details to medicines.csv")
