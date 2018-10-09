from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import csv, os, time
from datetime import datetime

from datetime import timedelta, date
start_date = date(2013, 1, 1)
end_date = date(2014, 1, 1)

currentTime = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
fileName = str(start_date.year)+"-"+str(start_date.month)+"_"+str(end_date.year)+"-"+str(end_date.month)+"_curr"+currentTime
leagueNames = set()

options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
#driver = webdriver.Firefox()
#actions = ActionChains(driver)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

with open("{0}.csv".format(fileName), "w") as csv_file:
	writer1 = csv.writer(csv_file)
	for date in daterange(start_date, end_date):
		driver.get("https://www.sofascore.com/football/{0}-{1}-{2}".format(str(date.year),str(date.month).zfill(2),str(date.day).zfill(2)))
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='js-event-list-table-container event-list']")))
		tournaments = driver.find_elements_by_class_name('tournament')
		print("******************************  " + date.strftime("%Y-%m-%d") + "  ******************************")
		for elem in tournaments:
			name = None
			category = None
			name = elem.find_elements_by_xpath('.//span[@class="tournament__name"]')
			category = elem.find_elements_by_xpath('.//span[@class="tournament__category"]')
			if len(name)>0:
				eventName = category[0].text.strip()+" "+ name[0].text.strip()
				if not eventName in leagueNames:
					try:
						writer1.writerow([eventName])
						leagueNames.add(eventName)
					except:
						print("Attempting to encode...")
						eventName = eventName.encode(encoding='UTF-8',errors='replace')
						eventName = eventName.decode('UTF-8')
						writer1.writerow([eventName])
						leagueNames.add(eventName)
					print(eventName)
		print("finished going through tournaments...")

driver.close()
