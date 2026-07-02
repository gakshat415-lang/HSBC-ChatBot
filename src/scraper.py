import os
import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from src.config import FUND_URLS, SCRAPED_DATA_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_with_retry(url, max_retries=3, base_delay=2):
    """Fetch URL with exponential backoff on failure."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"  Retry {attempt + 1}/{max_retries} in {delay}s: {e}")
                time.sleep(delay)
            else:
                print(f"  FAILED after {max_retries} attempts: {url}")
                return None

def extract_fund_data(soup, url):
    """Extract required fund data using BeautifulSoup and JSON parsing."""
    script = soup.find('script', id='__NEXT_DATA__')
    if not script:
        return "Failed to find __NEXT_DATA__"
        
    try:
        data = json.loads(script.string)
        mf = data['props']['pageProps']['mfServerSideData']
    except Exception as e:
        return f"Failed to parse JSON or extract mfServerSideData: {e}"

    fund_name = mf.get('scheme_name', 'N/A')
    category = f"{mf.get('category', 'N/A')} - {mf.get('sub_category', 'N/A')}"
    
    risk_level = mf.get('nfo_risk', 'N/A')
    if risk_level == 'N/A':
        stats = mf.get('stats', [])
        for stat in stats:
            if stat.get('id') == 'risk':
                risk_level = stat.get('value', 'N/A')
                break

    nav = mf.get('nav', 'N/A')
    nav_date = mf.get('nav_date', 'N/A')
    
    expense_ratio = mf.get('expense_ratio', 'N/A')
    if expense_ratio != 'N/A':
        expense_ratio = f"{expense_ratio}%"
        
    exit_load = mf.get('exit_load', 'N/A')
    min_sip = mf.get('min_sip_investment', 'N/A')
    if min_sip != 'N/A':
        min_sip = f"₹{min_sip}"
        
    min_lumpsum = mf.get('min_investment_amount', 'N/A')
    if min_lumpsum != 'N/A':
        min_lumpsum = f"₹{min_lumpsum}"
        
    benchmark = mf.get('benchmark_name', 'N/A')
    
    fund_manager = "N/A"
    fm_details = mf.get('fund_manager_details', [])
    if fm_details:
        fund_manager = ", ".join([fm.get('name', 'N/A') for fm in fm_details])
        
    aum = mf.get('aum', 'N/A')
    if aum != 'N/A':
        aum = f"₹{aum} Cr"
        
    launch_date = mf.get('launch_date', 'N/A')
    
    objective = mf.get('description', 'N/A')
    
    # Holdings
    holdings_list = mf.get('holdings', [])
    holdings_str = ""
    for i, h in enumerate(holdings_list[:10], 1): # Top 10
        name = h.get('company_name', 'N/A')
        corpus_per = h.get('corpus_per', 'N/A')
        holdings_str += f"{i}. {name} - {corpus_per}%\n"
    if not holdings_str:
        holdings_str = "N/A"

    scrape_date = datetime.now().strftime("%Y-%m-%d")
    
    text = f"""Fund Name: {fund_name}
Source URL: {url}
Scrape Date: {scrape_date}

Category: {category}
Risk Level: {risk_level}

NAV: ₹{nav} (as of {nav_date})

Expense Ratio: {expense_ratio}
Exit Load: {exit_load}
Minimum SIP: {min_sip}
Minimum Lumpsum: {min_lumpsum}
Benchmark: {benchmark}
Fund Manager: {fund_manager}
AUM: {aum}
Launch Date: {launch_date}

Investment Objective:
{objective}

Top Holdings:
{holdings_str}"""

    return text

def save_to_file(slug, clean_text):
    os.makedirs(SCRAPED_DATA_DIR, exist_ok=True)
    filepath = os.path.join(SCRAPED_DATA_DIR, f"{slug}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean_text)

def scrape_all_funds():
    """Scrape all 12 fund URLs and save clean text files."""
    results = {"success": [], "failed": []}

    for url in FUND_URLS:
        slug = url.split("/")[-1]
        print(f"Scraping: {slug}...")

        response = fetch_with_retry(url)
        if not response:
            results["failed"].append(slug)
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        clean_text = extract_fund_data(soup, url)
        if clean_text.startswith("Failed"):
            print(f"  {clean_text}")
            results["failed"].append(slug)
        else:
            save_to_file(slug, clean_text)
            results["success"].append(slug)

        time.sleep(1)

    print(f"\\nDone: {len(results['success'])} success, {len(results['failed'])} failed")
    return results

if __name__ == "__main__":
    scrape_all_funds()
