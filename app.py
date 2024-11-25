from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import dns.resolver
import tldextract
import time

# Flask app initialization
app = Flask(__name__)

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client["dns_info_db"]
dns_collection = db["dns_info"]

# Selenium WebDriver setup for Edge
edge_options = Options()
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")  # For better compatibility in headless mode
webdriver_service = Service(r"C:\Users\chara\OneDrive\Desktop\Detect_DNS\msedgedriver.exe")  # Update with the correct path

def get_dns_info(url):
    try:
        # Extract subdomain, domain, and TLD
        extracted = tldextract.extract(url)
        subdomain = extracted.subdomain
        domain = extracted.domain
        tld = extracted.suffix
        full_domain = f"{domain}.{tld}"

        # Fetch DNS records
        dns_records = dns.resolver.resolve(full_domain, "A")
        ip_addresses = [record.to_text() for record in dns_records]

        return {
            "subdomain": subdomain,
            "domain": domain,
            "top_level_domain": tld,
            "ip_addresses": ip_addresses
        }
    except Exception as e:
        return {"error": f"DNS error: {str(e)}"}


def search_google_and_get_url(search_term):
    try:
        driver = webdriver.Edge(service=webdriver_service, options=edge_options)
        driver.get("https://www.google.com")

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_term)
        search_box.submit()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
        )

        first_result = driver.find_element(By.CSS_SELECTOR, "h3")
        url = first_result.find_element(By.XPATH, "..").get_attribute("href")
        driver.quit()
        return url
    except Exception as e:
        return {"error": f"Search error: {str(e)}"}

@app.route("/search", methods=["POST"])
def search_and_store():
    try:
        data = request.json
        search_term = data.get("search_term")

        if not search_term:
            return jsonify({"error": "Search term is required"}), 400

        url = search_google_and_get_url(search_term)
        if isinstance(url, dict) and "error" in url:
            return jsonify(url), 500

        dns_info = get_dns_info(url)
        if "error" in dns_info:
            return jsonify({"error": dns_info["error"]}), 500

        dns_collection.update_one(
            {"domain": dns_info["domain"]},
            {"$set": dns_info},
            upsert=True
        )

        return jsonify({"message": "DNS info stored successfully", "data": dns_info}), 201
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/dns-info", methods=["GET"])
def get_dns_data():
    try:
        dns_data = list(dns_collection.find({}, {"_id": 0}))
        return jsonify(dns_data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
