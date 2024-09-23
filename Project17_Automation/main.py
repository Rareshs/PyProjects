from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import random

random_part = ''.join([str(random.randint(0, 9)) for _ in range(8)])
tel_nr = '40' + random_part
# print(tel_nr)



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://demoqa.com/automation-practice-form/")

name_field= WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[1]/div[2]/input'))
)
name_field.click()
name_field.send_keys('Rares')

last_name_field=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[1]/div[4]/input'))
)
last_name_field.click()
last_name_field.send_keys('Gabriel')

email_field=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[2]/div[2]/input'))
)
email_field.click()
email_field.send_keys('email@test.com')

gender_label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//label[@for="gender-radio-1"]'))
    )
gender_label.click() 

phone_field=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[4]/div[2]/input'))
)
phone_field.click()
phone_field.send_keys(tel_nr)
time.sleep(1)

dob_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[5]/div[2]/div[1]/div/input'))
)
dob_field.send_keys(Keys.CONTROL,'a')
dob_field.send_keys('05 Oct 2005') 

time.sleep(1)
#Subject-dropdown
subjects_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "subjects-auto-complete__value-container"))
)
subjects_container.click()
time.sleep(1)


subject_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "subjectsInput"))
)
subject_input.send_keys('Maths')
time.sleep(1)

first_option = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'subjects-auto-complete__option')]"))
)
first_option.click()

second_option=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "subjectsInput"))
)

subject_input.send_keys('Computer Science')
time.sleep(1)


second_option = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'subjects-auto-complete__option')]"))
)
second_option.click()


label = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[@for='hobbies-checkbox-2']"))
)

label.click()


pic_upload=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID,'uploadPicture'))
)
pic_upload.send_keys(r"C:\Users\User\Downloads\Pic1.jpg")

adress_text=WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div[2]/form/div[9]/div[2]/textarea'))
)
adress_text.click()
adress_text.send_keys('Str.Aviatorului, Nr.25C')


state_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "state"))
)
state_dropdown.click()

input_field_state = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "react-select-3-input"))
)

input_field_state.send_keys("Haryana")
time.sleep(1)  # Give it a moment to process
input_field_state.send_keys(Keys.ENTER)

city_dropdown=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID,'city'))
)
city_dropdown.click()

input_field_city = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'react-select-4-input'))
)
input_field_city.send_keys('Karnal')
time.sleep(1)
input_field_city.send_keys(Keys.ENTER)



#Submit case
submit=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID,'submit'))
)
submit.click()


time.sleep(6)
close_form=WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,'closeLargeModal'))
)

close_form.click()
time.sleep(1)
driver.quit()