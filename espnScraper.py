from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


import csv, os, time

from datetime import timedelta, date, datetime
start_date = date(2014, 9, 1)
end_date = date(2018, 5, 1)
acceptTournaments = set()
#matches = []
currentTime = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
fileName = str(start_date.year)+"-"+str(start_date.month)+"_"+str(end_date.year)+"-"+str(end_date.month)+"_curr"+currentTime

mistakeNum = 0

#options = Options()
#options.set_headless(headless=True)
#driver = webdriver.Firefox(firefox_options=options)
driver = webdriver.Firefox()
#actions = ActionChains(driver)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def gIHTML(item):
	return item.get_attribute('innerHTML')

#with open("{0}.csv".format(fileName), "w") as csv_file:
	#writer1 = csv.writer(csv_file)
	#writer1.writerow([])
#	try:
	#print("Opened writer!")
for date in daterange(start_date, end_date):
	t = time.time()
	driver.set_page_load_timeout(10)

	print(date.year, date.month, date.day)
	try:
	    driver.get("http://www.espn.com/soccer/scoreboard/_/league/all/date/{0}{1}{2}".format(date.year,str(date.month).zfill(2),str(date.day).zfill(2)))
	    print("Loaded!")
	except TimeoutException:
	    driver.execute_script("window.stop();")
	print('Time consuming:', time.time() - t)
	#WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "events")))
	divContainer = driver.find_elements_by_id('events')
	#print("******************************  " + date.strftime("%Y-%m-%d") + "  ******************************")
	tournaments = divContainer[0].find_elements_by_xpath('./a[@class="date-heading js-show"]')
	if len(tournaments)>0:
		for ind in range(len(tournaments)-1):
			print(str(ind))
			matches = tournaments[ind].find_elements_by_xpath('./article[@class="scoreboard soccer fallback js-show"]/following::tournaments[ind]/preceding::tournaments[ind+1]')
			print("matches:", matches)
			for match in matches:
				mainInfo = match.find_element_by_xpath('.//div[@class="competitors"]')

				teamA = mainInfo.find_element_by_xpath('./div[@class="team team-a"]')
				teamAName = gIHTML(teamA.find_element_by_xpath('./div[@class="team-container"]/div/div[@class="team-info"]/div/a[@name="&lpos=soccer:scoreboard:team"]/span[@class="short-name"]'))
				teamAScore = teamA.find_element_by_xpath('./div[@class="score-container"]/span').text

				teamB = mainInfo.find_elements_by_xpath('./div[@class="team team-b"]')
				teamBName = gIHTML(teamB.find_element_by_xpath('./div[@class="team-container"]/div/div[@class="team-info"]/div/a[@name="&lpos=soccer:scoreboard:team"]/span[@class="short-name"]'))
				teamBScore = teamB.find_element_by_xpath('./div[@class="score-container"]/span').text

				matchStatus = gIHTML(mainInfo.find_elements_by_xpath('./div[@class="game-status"]/span[@class="game-time"]'))

				print(teamAName, teamAScore, teamBName, teamBScore, matchStatus )
	else:
		print("No good")
	

driver.close()


