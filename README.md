# Apollo Pharmacy Scraper

This Python script scrapes medicine data from Apollo Pharmacy's website using its internal search API and product pages. It searches for medicines based on a term (e.g., "paracetamol") and pincode, collecting details for up to 70 in-stock products and saving them to a CSV file.

## 🔍 Features
- **Extracts the following details for each product**:
  - **Name**: Product name (e.g., "Dolo-650 Tablet 15's").
  - **MRP**: Maximum Retail Price.
  - **Selling Price**: Discounted price (if available).
  - **Tags**: Categories like Fever, Pain Relief, etc.
  - **Product ID**: Unique identifier for the product.
  - **SKU**: Stock Keeping Unit code.
  - **Product Link**: URL to the product page.
  - **About**: Description of the product (e.g., what it is and its uses).
  - **Uses**: Specific uses of the medicine (e.g., fever, pain relief).
  - **Directions for Use**: Instructions for taking the medicine.
  - **Medicinal Benefits**: Benefits of the medicine (e.g., pain relief, fever reduction).
  - **How It Works**: Mechanism of action (e.g., how it reduces pain or fever).
  - **Images**: Comma-separated URLs of product images.
- **Filters out** out-of-stock items to ensure only available products are included.
- **Uses Apollo’s internal API** for searching products and scrapes product pages for detailed information.
- **Error Handling**: Handles missing data, HTTP errors, and exceptions gracefully, marking fields as "N/A", "Failed to fetch", or "Error" as appropriate.

## 📦 Output
A CSV file named `scraped_medicines_data.csv` containing data for up to 70 in-stock medicines, with columns for all extracted fields (Name, MRP, SellingPrice, Tags, product_id, SKU, product_link, About, Uses, DirectionsForUse, MedicinalBenefits, HowItWorks, Images).

## ⚠️ Note on Authorization
This scraper uses a temporary local authorization token to access Apollo Pharmacy's internal search API. This token is:

Extracted from the Network tab in browser developer tools while using apollopharmacy.in

Session-based and may expire or vary across users and browsers

If the script stops working, replace the authorization header in the code with a fresh one from your browser session.

