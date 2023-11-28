#create the file modernhealthcare.py

# name matches domain name
# this is site specific login info
print("logging in to modernhealthcare")

# get to a preset login url
# go to home page
driver.get("https://www.modernhealthcare.com/")

login_button = driver.find_element_by_xpath('//*[@id="block-cmh-subscribe"]/ul/li[2]/a').click()
# enter email             
driver.find_element_by_xpath('//*[@id="username"]').send_keys("BI_VOX@pfizer.com")
# enter password
driver.find_element_by_xpath('//*[@id="password"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('//*[@id="login-submit"]').click()