#create the file pharmajapan.py

# name matches domain name
# this is site specific login info
print("logging in to PharmaJapan")

# get to a preset login url
# go to home page
driver.get("https://pj.jiho.jp/")

login_button = driver.find_element_by_xpath('//*[@id="js-pc-user-login"]/div/ul/li[1]/a/span').click()
# enter email             
driver.find_element_by_xpath('//*[@id="edit-name"]').send_keys("BI_VOX@pfizer.com")
# enter password
driver.find_element_by_xpath('//*[@id="edit-pass"]').send_keys("BIProject2023!")
# login
driver.find_element_by_xpath('//*[@id="edit-submit"]/span').click()