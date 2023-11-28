# name matches domain name
# this is site specific login info
print("logging in to endpts")

# get to a preset login url
# go to home page
driver.get("https://endpts.com/")

login_button = driver.find_element_by_xpath('/html/body/header/div/div/div[3]/div/ul/li[2]/button').click()
# enter email
driver.find_element_by_xpath('//*[@id="epn_sign_in_modal_email"]').send_keys("BI_VOX@pfizer.com")
# enter password
# TODO set a password so this works
driver.find_element_by_xpath('//*[@id="epn_sign_in_modal_password"]').send_keys("BIProject2023!")

# login
driver.find_element_by_xpath('//*[@id="epn_sign_in_modal_submit"]').click()

print('login success')

