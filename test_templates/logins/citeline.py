#create the file citeline.py

# name matches domain name
# this is site specific login info
print("logging in to citeline")

# get to a preset login url
# go to home page
driver.get("https://medtech.citeline.com/")

login_button = driver.find_element_by_xpath('/html/body/header/div[3]/div[5]/div[1]/div[3]/div[2]/span').click()
# enter email             
driver.find_element_by_xpath('//*[@id="username"]').send_keys("BI_VOX@pfizer.com")
# enter password
#driver.find_element_by_xpath('//*[@id="Password"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('//*[@type="submit"]').click()