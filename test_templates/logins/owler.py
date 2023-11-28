#create the file owler.py

# name matches domain name
# this is site specific login info
print("logging in to owler")

# get to a preset login url
# go to home page
driver.get("https://www.owler.com/corp")

login_button = driver.find_element_by_xpath('//*[@id="header"]/div[2]/div[4]/div[2]/div[1]/div[2]/div/nav/div[5]/a').click()
# enter email             
driver.find_element_by_xpath('//*[@id="email"]').send_keys("BI_VOX@pfizer.com")
# enter password
driver.find_element_by_xpath('//*[@id="password"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/button[1]').click()
