#create the file globaldata.py

# name matches domain name
# this is site specific login info
print("logging in to globaldata")

# get to a preset login url
# go to home page
driver.get("https://www.globaldata.com//")

login_button = driver.find_element_by_xpath('/html/body/nav/div[1]/div[1]/div[2]/div[1]/ul/li/a/span').click()
# enter email             
driver.find_element_by_xpath('//*[@id="EmailAddress"]').send_keys("BI_VOX@pfizer.com")
# enter password
driver.find_element_by_xpath('//*[@id="Password"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('//*[@id="btnlogin"]').click()