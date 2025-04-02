import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_band_stats(text):
    """
    Parses a multi-line string of band stats into a dictionary.
    """
    lines = text.strip().splitlines()
    stats = {}
    for i in range(0, len(lines), 2):
        key = lines[i].rstrip(":").strip()  # Remove colon and extra whitespace.
        value = lines[i + 1].strip() if i + 1 < len(lines) else ""
        stats[key] = value
    return stats


options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument("window-size=1920,1080")
# options.add_argument("zoom-factor=0.1")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

input_csv = "/home/aosousa/Dropbox/1_PORTFOLIO/metal_archives_brasil/src/metal_archives_brasil_links.csv"  # CSV file should contain a column named "url"
df_urls = pd.read_csv(input_csv)

for idx, row in df_urls.iterrows():
    url = row["URL"]
    print(f"Processing: {url}")
    driver.get(url)

    try:
        band_stats_elem = wait.until(
            EC.presence_of_element_located((By.ID, "band_stats"))
        )
        band_stats_text = band_stats_elem.text
    except Exception as e:
        print(f"Error retrieving band stats for {url}: {e}")
        band_stats_text = ""

    stats_dict = parse_band_stats(band_stats_text)
    stats_dict["url"] = url

    df_result = pd.DataFrame([stats_dict])

    if idx == 0:
        df_result.to_csv("output.csv", sep="\t", index=False, mode="w", header=True)
    else:
        df_result.to_csv("output.csv", sep="\t", index=False, mode="a", header=False)

    time.sleep(1)

driver.quit()
