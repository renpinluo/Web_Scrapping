#create the file statnews.py

# name matches domain name
# this is site specific login info
print("logging in to statnews")

# get to a preset login url
# go to home page
driver.get("https://www.statnews.com/")

login_button = driver.find_element_by_xpath('//*[@id="menu-subscribers-nav"]/li[2]/a').click()
# enter email
driver.find_element_by_xpath('//*[@id="login-email"]').send_keys("BI_VOX@pfizer.com")
# enter password
driver.find_element_by_xpath('//*[@id="login-password"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('//*[@id="login"]/form[1]/div[3]/input').click()