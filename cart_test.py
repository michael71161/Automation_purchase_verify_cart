#we will go to ecommerce page. type something on the search box,
#will add to cart all that will appear,then go to checkout
#at the checkout we will apply a disscout code get a disscount
#also we will validate: correct products in the cart , total price , price after discount

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

expectedProds = ['Cauliflower - 1 Kg', 'Carrot - 1 Kg', 'Capsicum','Cashews - 1 Kg']
actualProds = []
service_obj = Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
driver.maximize_window() #to make large browser window

#adding implicitly wait, may be redused
driver.implicitly_wait(5)
driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
time.sleep(3)
#get on screen all products that have ca in the name 
driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search for Vegetables and Fruits']").send_keys("ca")
time.sleep(5)
#store the products which we see after search 
products = driver.find_elements(By.XPATH, "//div[@class='products']/div")
print(f"number of products found:  {len(products)}")
assert len(products) > 0


#Click add to cart for all products
#Grab each product name for future validation

for prod in products:
    actualProds.append(prod.find_element(By.XPATH, "h4").text)  #grabing prod name for assertion 
    prod.find_element(By.XPATH, "div/button").click()  #chaining from parent to child in prod
 
assert  expectedProds == actualProds , "Products names arent matching, error"
#time.sleep(3)

#now  click go to cart 
driver.find_element(By.CSS_SELECTOR, "img[alt='Cart']").click()
#time.sleep(2)

# click proceed to checkout
    
driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()
#time.sleep(5) 

#**sum validation
prices = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(5) p")
priceSum = 0
for price in prices:
    priceSum = priceSum + int(price.text)
    
print(priceSum)
sumToCheck = int(driver.find_element(By.CSS_SELECTOR,".totAmt").text)
#assert following condition , if false - program will crash with the following error message 
assert priceSum == sumToCheck ,"sum of prices arent matching , error"



#next step apply disscount code
driver.find_element(By.CSS_SELECTOR,"input[placeholder='Enter promo code']").send_keys("rahulshettyacademy")
#time.sleep(5) 

#click on apply, we will use class so .before if we searching by css selector
driver.find_element(By.CSS_SELECTOR,".promoBtn").click()
#time.sleep(8)  #to let us see whats up

#applying explicit wait
#wait 15 seconds or until the apply prompt will appear which is unvisible before the apply
wait = WebDriverWait(driver,15)
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".promoInfo")))
#print the appeared element text
messageOnApply= driver.find_element(By.CLASS_NAME, 'promoInfo').text #unlike by css selector ,by class name no need of . before name
print(f"message on clicking apply: {messageOnApply}")

#assert that price after discount is less then initial price before cuppon 
sumDiscounted= float(driver.find_element(By.CSS_SELECTOR, ".discountAmt").text)

assert sumDiscounted < priceSum , "Problem with discount"


time.sleep(5) #visual confirmation to see discount







driver.close()