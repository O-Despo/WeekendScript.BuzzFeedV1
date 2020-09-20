import requests
import re
import codecs
import csv 
import time

"""
||||||||||||||||||||||||||||||||||||||||||||||
||         Buzzfeed data pareser            ||
||                 made by                  ||
||                 Odespo                   ||
||||||||||||||||||||||||||||||||||||||||||||||
"""

begin = time.time()
#Ranges change these
startYear = 2020
endYear = 2020

startDay = 18
endDay = 19

startMonth = 9
endMonth = 9


#Files save names and default start url
baseArchiveUrl = 'https://www.buzzfeed.com/archive/'
csvTitleUrl = "urlsAndTitles.csv"
outCsvQuizName = "quizTitleList.csv"


#Open or create files 
#note the mode "w+" will lead to files being overwired 
#BE CAREFULL AND MAKE BAKE UPS 
initial_run_out = open(csvTitleUrl, mode='w+', newline='')
initial_run_write = csv.writer(initial_run_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csvUrlsAndTitlesForInput = open(csvTitleUrl, mode="r", newline='')
csv_input_all_titles = csv.reader(csvUrlsAndTitlesForInput, delimiter=',')

#Opens the csv for only quiz output 
outCsv = open(outCsvQuizName, "w+", newline='')
csvWite = csv.writer(outCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csvQuiz = open(outCsvQuizName, "r", newline='')
csvQuizRead = csv.reader(csvQuiz, delimiter=',')


"""
Section 1 
Produce all the links for archive date withen range 
go through those links and find all the sub links 
"""
def getAllURLsFromArchive(baseUrl):
    
    #+ 1 so it run up to the end of the range I use while but they are pretest not post test 
    yearRange = range(startYear, endYear + 1)
    monthRange = range(startMonth, endMonth  + 1)
    dayRange = range(startDay, endDay + 1)

    #Produce the urls to grab 
    for year in yearRange:
        for month in monthRange:
            for day in dayRange:
                
                #Combines current urls to be requested
                currentArchiveUrl = baseArchiveUrl + str(year) + "/" + str(month) + "/" + str(day)
                date = str(year) + "/" + str(month) + "/" + str(day)
                currentPage = requests.get(currentArchiveUrl)
                print(currentArchiveUrl)

                #Send page to be processed 
                findURLsAndTitlesSave(currentPage.text, date)

                
def findURLsAndTitlesSave(textOfCurrnetPage, date):
    
    #Define regex compiles and shearch 
    titlePattern = re.compile(r"s=\"true\">(.*?)<\/")
    urlPattern = re.compile(r"y\" href=\"(.*?)\"\n")
    
    TitleList = re.findall(titlePattern, textOfCurrnetPage)
    UrlList = re.findall(urlPattern, textOfCurrnetPage)

    #Call to save the list of urls 
    saveToCSV(TitleList, UrlList, date)

def saveToCSV(FirstColRow, SecondColRow, date):
    i = 0

    while (i < len(FirstColRow)):
        try: 
            initial_run_write.writerow([FirstColRow[i], SecondColRow[i], date])
        except:
            pass
        i += 1



"""
Section 2 
Find all the quiz's from the section 1 run 
And pull data 
"""
def look_through_csv_for_quizs():
    
    #Define the regex patter for dates, name, and postion 
    datePattern = re.compile(r"8..Po.*?>.*?>(.*?)<\/s")
    authorPattern = re.compile(r"GCD\">(.*?)</")
    staffPostionPatten = re.compile(r"n><p>(.*?)<\/")
    descriptionPattern = re.compile(r"8q.>(.*?)<\/")
    catagoriesPattern = re.compile(r"58\">.*?>(.*?)<")

    for row in csv_input_all_titles:
        print(row[1])
        if (row.count("buzzfeednews") < 1):
            #Get page request
            pageCall = requests.get(row[1])
            pageText = pageCall.text

            #Find if quiz and date code
            quizBool = pageText.count('alt="Quiz badge"')
            #The numerical and more easily processed dates are one the sheet before if you want written out dates use un comment this 
            #datePosted = re.findall(datePattern, pageText)
            nameOfAuthor = re.findall(authorPattern, pageText)
            staffPosition = re.findall(staffPostionPatten, pageText)
            description = re.findall(descriptionPattern, pageText)
            catagories = re.findall(catagoriesPattern, pageText)
            
            if (quizBool == 1):
                
                #Try to write with date if not do not write 
                try:
                    csvWite.writerow([row[1], row[0], row[2], catagories[1], nameOfAuthor, staffPosition, description[0]])
                except:
                    csvWite.writerow(row)
                
                print("quiz")
            
            else:
                pass
        else:
            pass

getAllURLsFromArchive(baseArchiveUrl)

look_through_csv_for_quizs()

end = time.time()

print (end - begin) 
