from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

url = 'https://rejstrik-firem.kurzy.cz/'
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

# Přijmutí cookies
accept_button = driver.find_element("xpath",
                                    '//*[contains(concat( " ", @class, " " ), concat( " ", "fc-button-label", " " ))]')
accept_button.click()


with open("ico_values.txt") as file:
    ico_list = file.readlines()

with open("companies_info.txt", "a", encoding="utf-8") as c_info:
    for ico in ico_list:
        ico = ico.strip()
        driver.get(url)

        field = driver.find_element("id", "id_s")
        field.send_keys(ico)
        field.send_keys(Keys.RETURN)

        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        try:
            info_table = driver.find_element("id", "orsmallinfotab").text
        except NoSuchElementException:
            c_info.write(F"IČO: {ico} PRAVDĚPODOBNĚ NEEXISTUJE")
            c_info.write("\n\n\n")
            continue
        name = re.search(r"NÁZEV(.*)", info_table)
        ic = re.search(r"IČO(.*)", info_table)
        form = re.search(r"FORMA(.*)", info_table)
        adress = re.search(r"ADRESA(.*)", info_table)

        if name:
            c_info.write(name.group() + "\n")
        if ic:
            c_info.write(ic.group() + "\n")
        if form:
            c_info.write(form.group() + "\n")
        if adress:
            c_info.write(adress.group() + "\n")

        try:
            contact_table = driver.find_elements(By.CSS_SELECTOR, "tbody")[2].text
            if re.search(r"TELEFON(.*)", contact_table):
                c_info.write(contact_table)
            else:
                c_info.write("Nenalezeny žádné kontaktní údaje.")
        except:
            c_info.write("Nenalezeny žádné kontaktní údaje.")

        c_info.write("\n\n\n")

driver.quit()
