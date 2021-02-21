import bs4
import sys
import requests
import csv
import re
from selenium import webdriver
import time

def convert(STR):
    titleRaw = html.select(STR)
    titleStr = titleRaw[0].text.strip()
    return titleStr





login = "login"     #type login and password here
password = "password"



driver = webdriver.Firefox(executable_path=r'C:\Users\Maciek\Downloads\geckodriver.exe')
driver.get('https://www.filmweb.pl/login')
time.sleep(5)
logButton = driver.find_element_by_css_selector(".authButton--filmweb > div:nth-child(2)")
logButton.click()

logInput = driver.find_element_by_css_selector("div.materialForm__textField:nth-child(1) > input:nth-child(1)")
passwordInput = driver.find_element_by_css_selector(".materialForm__input--icon")
logInput.send_keys(login)
passwordInput.send_keys(password)
passwordInput.submit()
time.sleep(10)



file1 = open("MyFile.csv", "a")
file1.write("Tytul;Moja_ocena;Srednia_ocena;Premiera;Rok;Liczba_glosow;Gatunek;Produkcja;Dlugosc;Rezyser\n")
file1.close()
page=0
index =1
while(page<65):
    file1 = open("MyFile.csv", "a")
    page+=1
    productName = "https://www.filmweb.pl/user/pigmej4ever/films?page={}".format(page)
    driver.get(productName)
    site =driver.page_source
    html = bs4.BeautifulSoup(site, 'html.parser')

    txt = html.text
    x = re.findall('"eId":[0-9]+', txt)

    xd = ''.join(x)
    x = re.findall('[0-9]+', xd)
    print(x)
    print(page)

    i=0
    rating_index=4;
    for i in range(len(x)):
        if(rating_index == 29):
            rating_index=4
        try:
            print(x[i])
            title = '#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h2:nth-child(1)'.format(
                x[i])
            year2 = '#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)'.format(x[i])
            year = '#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(3)'.format(x[i])
            counts = '#filmPreview_{} > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(4)'.format(
                x[i])
            director = '#filmPreview_{} > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div:nth-child(3) > ul:nth-child(2) > li:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > span:nth-child(1)'.format(
                x[i])
            genre = '#filmPreview_{} > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > h3:nth-child(1) > a:nth-child(1)'.format(
                x[i])
            rating = '#filmPreview_{} > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)'.format(
                x[i])
            my_rating = 'div.voteBoxes__box:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)'.format(
                rating_index)


            durationStr="NaN"
            ProductionStr="NaN"
            premiereStr="NaN"

            titleStr = convert(title)
            print(titleStr)

            yearStr = convert(year)
            year2Str = convert(year2)
            if (yearStr.isnumeric() == False):
                if (year2Str.isnumeric() == True):
                    yearStr = year2Str
                else:
                    yearStr = "NaN"
            print(yearStr)

            productName = "https://www.filmweb.pl/film/{}-{}-{}".format(titleStr.replace(' ', '+'), yearStr, x[i])
            print(productName)
            site2 = requests.get(productName)
            temp = bs4.BeautifulSoup(site2.text, 'html.parser')

            production2 = 'div.filmInfo__info:nth-child(9) > span:nth-child(1) > a:nth-child(1)'
            production = 'div.filmInfo__info:nth-child(8) > span:nth-child(1) > a:nth-child(1)'

            productionRaw = temp.select(production)
            ProductionStr = productionRaw[0].text.strip()
            print(ProductionStr)

            countsStr = convert(counts)
            if (countsStr.replace(' ', '').isnumeric() == False):
                countsStr = "Nan"
            print(countsStr)
            directorStr = convert(director)
            print(directorStr)
            genreStr = convert(genre)
            print(genreStr)
            ratingStr = convert(rating)
            print(ratingStr)
            my_ratingStr = convert(my_rating)
            if (my_ratingStr.isnumeric() == False):
                my_ratingStr = "NaN"
            print(my_ratingStr)



            duration = '.filmCoverSection__filmTime'
            premiere = '.block'


            durationRaw = temp.select(duration)
            durationStr = durationRaw[0].text.strip()
            print(durationStr)


            premiereRaw = temp.select(premiere)
            premiereStr = premiereRaw[0].text.strip().replace(" (świat)", "")
            print(premiereStr)


            file1.write(titleStr+';'+my_ratingStr.replace(',','.')+';'+ratingStr.replace(',','.')+';'+premiereStr+';'+yearStr+';'+countsStr+';'+genreStr+';'+ProductionStr+';'+durationStr+';'+directorStr+'\n')
            rating_index+=1
        except:
            try:
                print('============================')
                print(x[i])
                title = '#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h2:nth-child(1)'.format(x[i])
                year='#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)'.format(x[i])
                year2 = '#filmPreview_{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(3)'.format(x[i])
                counts='#filmPreview_{} > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(4)'.format(x[i])
                director='#filmPreview_{} > div:nth-child(2) > div:nth-child(4) > div:nth-child(3) > div:nth-child(3) > ul:nth-child(2) > li:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > span:nth-child(1)'.format(x[i])
                genre='#filmPreview_{} > div:nth-child(2) > div:nth-child(4) > div:nth-child(3) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > h3:nth-child(1) > a:nth-child(1)'.format(x[i])
                rating='#filmPreview_{} > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)'.format(x[i])
                my_rating='div.voteBoxes__box:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)'.format(rating_index)




                titleStr=convert(title)
                print(titleStr)
                yearStr=convert(year)
                year2Str=convert(year2)
                if (yearStr.isnumeric() == False):
                    if(year2Str.isnumeric() == True):
                        yearStr = year2Str
                    else:
                        yearStr="NaN"
                print(yearStr)
                productName = "https://www.filmweb.pl/film/{}-{}-{}".format(titleStr.replace(' ', '+'), yearStr, x[i])
                print(productName)
                site2 = requests.get(productName)
                temp = bs4.BeautifulSoup(site2.text, 'html.parser')

                durationStr = "NaN"
                ProductionStr = "NaN"
                premiereStr = "NaN"


                production = 'div.filmInfo__info:nth-child(8) > span:nth-child(1) > a:nth-child(1)'
                production2 = 'div.filmInfo__info:nth-child(9) > span:nth-child(1) > a:nth-child(1)'


                productionRaw = temp.select(production)
                ProductionStr = productionRaw[0].text.strip()
                print(ProductionStr)

                countsStr=convert(counts)
                if ( countsStr.replace(' ','').isnumeric() == False):
                    countsStr = "Nan"
                print(countsStr)
                directorStr=convert(director)
                print(directorStr)
                genreStr=convert(genre)
                print(genreStr)
                ratingStr=convert(rating)
                print(ratingStr)
                my_ratingStr=convert(my_rating)
                if (my_ratingStr.isnumeric() == False):
                    my_ratingStr = "NaN"
                print(my_ratingStr)





                duration = '.filmCoverSection__filmTime'
                premiere = '.block'

                durationRaw = temp.select(duration)
                durationStr = durationRaw[0].text.strip()
                print(durationStr)


                premiereRaw = temp.select(premiere)
                premiereStr = premiereRaw[0].text.strip().replace(" (świat)", "")
                print(premiereStr)


                file1.write(titleStr+';'+my_ratingStr.replace(',','.')+';'+ratingStr.replace(',','.')+';'+premiereStr+';'+yearStr+';'+countsStr+';'+genreStr+';'+ProductionStr+';'+durationStr+';'+directorStr+'\n')
                rating_index+=1
            except:
                pass
    print('Download finished')
    file1.close()

