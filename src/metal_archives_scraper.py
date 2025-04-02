from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# OBJETIVO: Construir um dataset de bandas brasileiras de metal a partir do repositório https://www.metal-archives.com/

options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-notifications")
options.add_argument("window-size=1920,1080")  # Set your desired window size
options.add_argument("zoom-factor=0.1")  # Set the desired zoom level (1.0 means 100%)

driver = webdriver.Chrome(options=options)

action = ActionChains(driver)

driver.get("https://www.metal-archives.com/lists/BR")

time.sleep(8)
table_data = []
links = []

max_attempts = 18
attempts = 0
next_button = driver.find_element(By.XPATH, '//*[@id="bandListCountry_next"]')
while next_button:

    table_rows = driver.find_elements(
        By.XPATH, "//table[@class='display dataTable']/tbody/tr"
    )
    time.sleep(3)
    for row in table_rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        links.append([link])
        row_data = [column.text for column in columns]
        table_data.append(row_data)
        pd.DataFrame(table_data).head()

    # next_button.click()
    if next_button.is_enabled():
        next_button.click()
        time.sleep(3)
    else:
        break

# Salva os resultados em um df e arquivo csv
df = pd.DataFrame(table_data, columns=["Band", "Genre", "Location", "Status"])

df.to_csv("metal_archives_brasil.csv", index_label="Index", index=False, sep="\t")

link_table = pd.DataFrame(links, columns=["URL"])
link_table.to_csv(
    "metal_archives_brasil_links.csv",
    index_label="Index",
    index=False,
)
driver.quit()
