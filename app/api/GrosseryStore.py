# import time 

# from selenium import webdriver 
# from selenium.webdriver import Chrome 
# from selenium.webdriver.chrome.service import Service 
# from selenium.webdriver.common.by import By 
# from webdriver_manager.chrome import ChromeDriverManager

# # start by defining the options 
# options = webdriver.ChromeOptions() 
# # we don't need it as the page also populated with the running javascript code. 
# options.page_load_strategy = 'none' 
# # this returns the path web driver downloaded 
# chrome_path = ChromeDriverManager().install() 
# chrome_service = Service(chrome_path) 
# # pass the defined options and service objects to initialize the web driver 
# driver = Chrome(options=options, service=chrome_service) 
# driver.implicitly_wait(5)



# def get_the_price_by_kg(url):
#     driver.get(url)
#     time.sleep(5)
#     price = driver.find_element(By.CSS_SELECTOR, "div[class*='price-per-um__pdp'")
#     if price:
#         price = price.text
#         price = ''.join(filter(str.isdigit, price))
#         price = int(price)
#     else:
#         price = "not found"
#     driver.quit()
#     return price