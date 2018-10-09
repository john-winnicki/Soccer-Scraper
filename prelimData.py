from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import csv, os, time

from datetime import timedelta, date, datetime
start_date = date(2014, 1, 1)
end_date = date(2018, 6, 1)
acceptTournaments = set()
tournamentSelectorOn = True
#matches = []
currentTime = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
fileName = str(start_date.year)+"-"+str(start_date.month)+"_"+str(end_date.year)+"-"+str(end_date.month)+"_curr"+currentTime

mistakeNum = 0
"""
options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
"""
driver = webdriver.Firefox()
#actions = ActionChains(driver)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def gIHTML(item):
	return item.get_attribute('innerHTML')

with open('tournamentFinal.csv') as csvfile:
	rowreader = csv.reader(csvfile)
	for row in rowreader:
		acceptTournaments.add(row[0])

with open("{0}.csv".format(fileName), "w") as csv_file:
	writer1 = csv.writer(csv_file)
	writer1.writerow(["Event Name","Date",	"Home team", "Away team", "Halftime", "Fulltime", "Overtime", "Extratime", "Home team scores [Scorer name, minute]", "Away team scores [Scorer name, minute]",	"Home team Penalty Shots [Penalty shooter name, Minute‚ Bool(Shot made)]",	
		"Away team Penalty Shots [Penalty shooter name, Minute, Bool(Shot made)]",	"Home Overtime [Bool(Shot made), Order]", "Away Overtime [Bool(Shot made), Order]", "Home Redcard [Red Cardee Name, Minute, Reason]", "Home Redcard [Red Cardee Name, Minute, Reason]",	"Home Past 5 Games", "Home Past 5 Games Total", "Score Away Past 5 Games", "Away Past 5 Games Total Score", "Home Manager", "Away Manager",	
		"Referee", "Referee Avg Yellow cards", "Referee Avg Red Cards", "Location", "Venue", "Attendance"])
#	try:
	#print("Opened writer!")
	for date in daterange(start_date, end_date):
		try:
			driver.get("https://www.sofascore.com/football/{0}-{1}-{2}".format(date.year,str(date.month).zfill(2),str(date.day).zfill(2)))
			WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".event-list")))
			tournaments = driver.find_elements_by_class_name('tournament')
			#print("******************************  " + date.strftime("%Y-%m-%d") + "  ******************************")
			for elem in tournaments:
				name = None
				category = None
				#print("Starting new League")
				name = elem.find_elements_by_xpath('.//span[@class="tournament__name"]')
				category = elem.find_elements_by_xpath('.//span[@class="tournament__category"]')
				if len(name)>0:
					eventName = category[0].text.strip()+" "+ name[0].text.strip()
					if eventName in acceptTournaments:
						print("Event in tournament:", eventName)
						#print("**************************************************************"+eventName)
						#print("............",category[0].text.strip(), name[0].text.strip(), "............")
						
						matchLink = elem.find_elements_by_xpath('.//div[@class="js-event-list-tournament-events"]/a')
						for matchup in matchLink:
							#versus = None
							matchHome = None
							matchAway = None
							
							noIncidentData = False
							headerContainer = ""

							halfScore = ""
							finalScore = ""
							overScore = ""
							extraScore = ""

							awayScore = []
							homeScore = []
							awayPenalty = []
							homePenalty = []
							awayOverTime = []
							homeOverTime = []
							awayRedCards = []
							homeRedCards = []

							homePast5Games = []
							homePast5GamesTotalScore = ""
							awayPast5Games = []
							awayPast5GamesTotalScore = ""

							homeManager = ""
							awayManager = ""

							matchReferee=""
							refAvgYellowCards = ""
							refAvgRedCards = ""
							matchLocation = ""
							matchVenue = ""
							matchAttendence = ""

							#versus = matchup.find_elements_by_xpath('.//div[@class="cell__section--main  "]/div')
							matchHome= gIHTML(matchup.find_elements_by_xpath('.//div[@class="cell__section--main  "]/div')[0]).strip()
							matchAway = gIHTML(matchup.find_elements_by_xpath('.//div[@class="cell__section--main  "]/div')[1]).strip()
							#print(matchHome, "Vs. ", matchAway)
							if matchHome.find("<span")>-1:
								matchHome = matchHome[:matchHome.find("<span")].strip()
							if matchAway.find("<span")>-1:
								matchAway = matchAway[:matchAway.find("<span")].strip()
							#print("Changed:", matchHome, "Vs. ", matchAway)
							#dataID = match.get_attribute("data-id")
							
							matchDataID = matchup.get_attribute('data-id')
							driver.execute_script("arguments[0].click();", matchup)
							#matchup.click()
							#time.sleep(1)

							try:
								WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="js-details-widget-container widget-container"]/div[@data-id={0}]'.format(matchDataID))))
							except:
								#print(gIHTML(matchup))
								driver.execute_script("arguments[0].click();", matchup)
								WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="js-details-widget-container widget-container"]/div[@data-id={0}]'.format(matchDataID))))
							WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "tab-event-widget-details")))
							contentContainer = driver.find_element_by_id('tab-event-widget-details')
							
							WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, './/div[@class="js-details-component-startTime-container"]//div[@class="cell__content"]')))
							startTime = contentContainer.find_element_by_xpath('.//div[@class="js-details-component-startTime-container"]//div[@class="cell__content"]').text
							#print(startTime)

							fullScore = contentContainer.find_elements_by_xpath('.//div[contains(@class, "incidents-container")]/div[contains(@class, "cell--center")]//div[@class="cell__content incident__period"]')
							for score in fullScore:
								score = gIHTML(score).strip()
								if score[0:2]=="FT":
									finalScore = score[3:]
									#print("Final score:", finalScore)
								elif score[0:2]=="HT":
									halfScore = score[3:]
									#print("halfScore:", halfScore)
								elif score[0:2]=="OT":
									overScore = score[3:]
									#print("overScore:", overScore)
								elif score[0:2]=="ET":
									extraScore = score[3:]
									#print("extraScore:", extraScore)
							if finalScore == "":
								try:
									print("Scraping small data")
									headerContainer = driver.find_element_by_xpath('.//div[@class="js-event-widget-header-container"]//div[@class="cell__section--main u-tC"]')
									print(headerContainer)
									finalScore = headerContainer.find_element_by_xpath('./div[@class="cell__content u-pT8"]/span').text
									print(finalScore)

								except:
									print("No finalScore found")
									continue

							if halfScore == "":
								try:
									print("Finding new halfscore!")
									headerContainer = driver.find_element_by_xpath('.//div[@class="js-event-widget-header-container"]//div[@class="cell__section--main u-tC"]')
									halfScore = headerContainer.find_elements_by_xpath('./div[@class="cell__content"]/span[@class="u-t2 u-t16"]')
									print("Halfscore:", halfScore)
									if len(halfScore)==0:
										print("No halfscore available!")
										halfScore = "N/A"
									else:
										halfScore = halfScore[0].text[1:-1]
								except:
									print("No halfscore found")
									continue
									#print(finalScore, halfScore)


							#Important lesson learned: You must put the entire class name in an xpath selector. You can't just put cell--center for example. Otherwise, use contains.

							#away = incidents.find_elements_by_xpath('.//div[@class="cell cell--right cell--incident"]')
							#home = incidents.find_elements_by_xpath('.//div[@class="cell cell--incident"]')
							penaltyOrder = 0

							try:
								print(startTime, "home:", matchHome, "away", matchAway)
								incidentContainer = contentContainer.find_element_by_xpath('.//div[@class="incidents-container"]')
							except:
								print("No Incident Data!")
								noIncidentData = True

							if noIncidentData==False:
								incidents = incidentContainer.find_elements_by_xpath('./div[contains(@class, "cell--incident")]')
								for elem in incidents:
									goals = elem.find_elements_by_xpath('.//div[contains(@title, "Goal")]')
									penalties = elem.find_elements_by_xpath('.//div[@title= "Penalty"]')
									missedPenalties = elem.find_elements_by_xpath('.//div[@title = "Missed Penalty"]')
									redCards = elem.find_elements_by_xpath('.//div[@title = "Red card"]')+elem.find_elements_by_xpath('.//div[@title = "2nd Yellow card (Red)"]')
									isAway = False
									if elem.get_attribute('class').find('right')>0:
										#print("isAway")
										isAway = True

									if len(goals)>0:
										try:
											scorer = elem.find_element_by_xpath('.//span[@class="incident__scorer"]/a')
											scorerName = scorer.get_attribute('data-player-name')
										except:
											#print(gIHTML(elem.find_element_by_xpath('.//span[@class="incident__scorer"]')))
											scorer = elem.find_elements_by_xpath('.//span[@class="incident__scorer"]/span')
											if len(scorer)==0:
												scorerName = "N/A"
											else:
												scorerName = scorer[0].get_attribute('data-player-name')
										scorerTime = gIHTML(elem.find_element_by_xpath('.//div[@class="cell__content incident__time"]')).strip()
										if scorerTime.find('<sup>')>-1:
											scorerTime = scorerTime.replace('<sup>','').replace('</sup>','')
										#print(scorerTime)
										if isAway == True:
											awayScore.append([scorerName, scorerTime])
										else: 
											homeScore.append([scorerName, scorerTime])
									elif len(penalties)>0:
										penaltyScorerTime =  gIHTML(elem.find_element_by_xpath('.//div[@class="cell__content incident__time"]')).strip()
										#print(penaltyScorerTime)
										if penaltyScorerTime.find('<sup>')>-1:
											penaltyScorerTime = penaltyScorerTime.replace('<sup>','').replace('</sup>','')
										if penaltyScorerTime != '-':
											try:
												penaltyScorerName = elem.find_element_by_xpath('.//span[@class="incident__scorer"]/a')
												penaltyScorerName = penaltyScorer.get_attribute('data-player-name')
											except:
												penaltyScorer = elem.find_elements_by_xpath('.//span[@class="incident__scorer"]/span')
												if len(penaltyScorer)==0:
													penaltyScorerName = "N/A"
												else:
													penaltyScorerName = penaltyScorer[0].get_attribute('data-player-name')
											if isAway ==True: 
												awayPenalty.append([penaltyScorerName, penaltyScorerTime, True])
											else:
												homePenalty.append([penaltyScorerName, penaltyScorerTime, True])
										else:
											if isAway ==True:
												awayOverTime.append([True, penaltyOrder+1])
												penaltyOrder+=1
											else:
												homeOverTime.append([True, penaltyOrder+1])
												penaltyOrder+=1
									elif len(missedPenalties) > 0:
										penaltyScorerTime =  gIHTML(elem.find_element_by_xpath('.//div[@class="cell__content incident__time"]')).strip()
										if penaltyScorerTime.find('<sup>')>-1:
											penaltyScorerTime = penaltyScorerTime.replace('<sup>','').replace('</sup>','')
										if penaltyScorerTime != '-':
											try:
												penaltyScorerName = gIHTML(elem.find_element_by_xpath('.//div[@class="cell__content"]//a')).strip()
											except:
												penaltyScorerName = elem.find_element_by_xpath('.//span').text
											if isAway ==True: 
												awayPenalty.append([penaltyScorerName, penaltyScorerTime, False])
											else:
												homePenalty.append([penaltyScorerName, penaltyScorerTime, False])
										else:
											if isAway == True:
												awayOverTime.append([False, penaltyOrder+1])
												penaltyOrder+=1
											else:
												homeOverTime.append([False, penaltyOrder+1])
												penaltyOrder+=1
									elif len(redCards)>0:
										try: 
											redCardTime =  gIHTML(elem.find_element_by_xpath('.//div[@class="cell__content incident__time"]')).strip()
											if redCardTime.find('<sup>')>-1:
												redCardTime = redCardTime.replace('<sup>','').replace('</sup>','')
										except:
											redCardTime = "OT"
										try:
											redCarder = elem.find_element_by_xpath('.//div[@class="cell__content h4"]/a')
											redCarderName = redCarder.get_attribute('data-player-name')
											if len(redCarderName) == 0:
												redCarderName = "N/A"
										except:
											#print("Red card exception")
											redCarder = elem.find_element_by_xpath('.//span')
											redCarderName = redCarder.text
											if len(redCarderName)==0:
												redCarderName = "N/A"
										try: 
											redCardReason = gIHTML(elem.find_element_by_xpath('.//span[@class="incident__dim"]')).strip()
										except:
											if len(elem.find_elements_by_xpath('.//div[@title = "2nd Yellow card (Red)"]'))>0:
												redCardReason = "2nd Yellow card"
											else:
												redCardReason = "N/A"
										if isAway==True:
											awayRedCards.append([redCarderName, redCardTime, redCardReason])
										else:
											homeRedCards.append([redCarderName, redCardTime, redCardReason])
								#print(homeScore, awayScore, homePenalty, awayPenalty, homeOverTime, awayOverTime, homeRedCards, awayRedCards)

							else:
								try:
									#print("Scraping small data")
									headerContainer = driver.find_element_by_xpath('.//div[@class="js-event-widget-header-container"]//div[@class="cell__section--main u-tC"]')
									print(headerContainer)
									finalScore = headerContainer.find_element_by_xpath('./div[@class="cell__content u-pT8"]/span').text
									print(finalScore)
									halfScore = headerContainer.find_elements_by_xpath('./div[@class="cell__content"]/span[@class="u-t2 u-t16"]')
									if len(halfScore)==0:
										print("No halfscore!")
										halfScore = "N/A"
									else:
										halfScore = halfScore[0].text[1:-1]
									#print(finalScore, halfScore)

								except:
									print("No data found")
									continue


							pGameForm = contentContainer.find_elements_by_xpath('.//div[@class="js-widget-teams-form widget-teams-form"]/div')
							if len(pGameForm)==3:
								PGameForm1 = pGameForm[1]
								PGameForm2 = pGameForm[2]
								name1 = gIHTML(PGameForm1.find_element_by_xpath('.//div[@class="cell__content standings__team-name"]')).strip()
								name2 = gIHTML(PGameForm2.find_element_by_xpath('.//div[@class="cell__content standings__team-name"]')).strip()
								past5Games1 = PGameForm1.find_elements_by_xpath('.//div[@class="cell__section standings__last-5"]/div/span')
								past5Games1Result = []
								for item in past5Games1:
									text = item.get_attribute('class')
									past5Games1Result.append(text[text.find('-')+1:])
								past5Games2 = PGameForm2.find_elements_by_xpath('.//div[@class="cell__section standings__last-5"]/div/span')
								past5Games2Result = []
								for item in past5Games2:
									text = item.get_attribute('class')
									past5Games2Result.append(text[text.find('-')+1:])
								score1 = gIHTML(PGameForm1.find_element_by_xpath('.//div[@class="cell__section standings__points"]/div')).strip()
								score2 = gIHTML(PGameForm2.find_element_by_xpath('.//div[@class="cell__section standings__points"]/div')).strip()
								if matchHome.find(name1)>-1:
									homePast5Games=past5Games1Result
									homePast5GamesTotalScore = score1
									awayPast5Games=past5Games2Result
									awayPast5GamesTotalScore = score2
									#print(matchHome, name1)
								elif matchAway.find(name1)>-1:
									homePast5Games=past5Games2Result
									homePast5GamesTotalScore = score2
									awayPast5Games=past5Games1Result
									awayPast5GamesTotalScore = score1
									#print(matchAway, name1)
								elif matchHome.find(name2)>-1:
									homePast5Games=past5Games2Result
									homePast5GamesTotalScore = score2
									awayPast5Games=past5Games1Result
									awayPast5GamesTotalScore = score1
									#print(matchHome, name2)
								elif matchAway.find(name2)>-1:
									homePast5Games=past5Games1Result
									homePast5GamesTotalScore = score1
									awayPast5Games=past5Games2Result
									awayPast5GamesTotalScore = score2
									#print(matchAway, name2)
								elif matchHome.find(name1[:2])>-1 and matchAway.find(name2[:2])>-1:
									homePast5Games=past5Games1Result
									homePast5GamesTotalScore = score1
									awayPast5Games=past5Games2Result
									awayPast5GamesTotalScore = score2
									#print(matchHome, name1)
								elif matchAway.find(name1[:2])>-1 and matchHome.find(name2[:2])>-1:
									homePast5Games=past5Games2Result
									homePast5GamesTotalScore = score2
									awayPast5Games=past5Games1Result
									awayPast5GamesTotalScore = score1
									#print(matchAway, name1)
								else:
									homePast5Games = "Can't tell!"
									awayPast5Games = "Can't tell!"
									homePast5GamesTotalScore = "Can't tell!"
									awayPast5GamesTotalScore = "Can't tell!"
									#print(matchHome, matchAway, name1, name2)

							h2hPages = contentContainer.find_elements_by_xpath('.//div[@class="js-event-page-h2h-container"]')
							if len(h2hPages)>0:
								for page in h2hPages:
									if len(page.find_elements_by_xpath('./h3'))>0 and gIHTML(page.find_element_by_xpath('./h3')).strip()=="Manager h2h":
										homeManager = gIHTML(page.find_element_by_xpath('.//div[@class="cell__section--main u-tL"]/div[@class="cell__content u-fs12"]')).strip()
										awayManager = gIHTML(page.find_element_by_xpath('.//div[@class="cell__section--main u-tR"]/div[@class="cell__content u-fs12"]')).strip()
										#print(homeManager, awayManager)


							matchInfo = contentContainer.find_elements_by_xpath('.//div[@class="js-event-page-info-container"]')
							if len(matchInfo)>0:
								tableItems = matchInfo[0].find_elements_by_xpath('.//table/tbody/tr')
								for item in tableItems:
									rowItem = item.find_elements_by_xpath('./td')
									if gIHTML(rowItem[0])=="Referee":
										matchReferee= gIHTML(rowItem[1]).strip()
										#print("matchReferee: ", matchReferee)
									elif gIHTML(rowItem[0]) == "Avg. cards":
										refAvgCards = gIHTML(rowItem[1]).strip()
										refAvgCards = refAvgCards[refAvgCards.find('</span>')+7:]
										refAvgRedCards = refAvgCards[:refAvgCards.find('<span')].strip()
										refAvgYellowCards = refAvgCards[refAvgCards.find('</span')+7:].strip()
										#print("refAvgRedCards:", refAvgRedCards)
										#print("refAvgYellowCards:", refAvgYellowCards)
									elif gIHTML(rowItem[0]) == "Location":
										matchLocation = gIHTML(rowItem[1]).strip()
										#print("Location: ", matchLocation)
									elif gIHTML(rowItem[0]) == "Venue":
										matchVenue = gIHTML(rowItem[1]).strip()
										#print("matchVenue: ", matchVenue)
									elif gIHTML(rowItem[0]) == "Attendance":
										matchAttendence = gIHTML(rowItem[1]).strip()
										#print("matchAttendence: ", matchAttendence)

							matchSummaries = [eventName, startTime, matchHome, matchAway, halfScore, finalScore, overScore, extraScore, homeScore, 
								awayScore, homePenalty, awayPenalty, homeOverTime, awayOverTime, homeRedCards, awayRedCards, homePast5Games, 
								homePast5GamesTotalScore, awayPast5Games, awayPast5GamesTotalScore, homeManager, awayManager, matchReferee, 
								refAvgYellowCards, refAvgRedCards, matchLocation, matchVenue, matchAttendence]
							a = []
							for item in matchSummaries:
								if item==[] or item =="" or item == ' ':
									a.append("N/A")
								else:
									a.append(item)

							writer1.writerow(a)
									
							print(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], 
								a[16], a[17], a[18], a[19], a[20], a[21], a[22], a[23], a[24], a[25], a[26], a[27])
					#else:
					#	print("Not acceptable tournament!")
		except:
			print("MISTAKE HAPPENED")
			mistakeNum += 1
			a = []
			for num in range(28):
				a.append("MISTAKE {0}".format(mistakeNum))
			writer1.writerow(a)

driver.close()


