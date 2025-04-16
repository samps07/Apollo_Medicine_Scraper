# Apollo Medicine Scraper

This Python script scrapes medicine data from Apollo Pharmacy's internal API using a specific search term and pincode. It collects 70 available (in-stock) products and saves the data into a CSV file.

## 🔍 Features

- Extracts:
  - Name
  - MRP (Maximum Retail Price)
  - Selling Price
  - Tags (like Fever, Pain Relief, etc.)
  - Product ID
  - SKU
  - Product Page URL
- Filters out **out-of-stock** items
- Uses Apollo’s internal API for structured results

## 📦 Output

A CSV file named `scraped_medicines_data.csv` containing data for 70 available medicines.

