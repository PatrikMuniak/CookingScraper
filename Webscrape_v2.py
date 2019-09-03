#!/usr/bin/env python3
#FOODY_SCRAPY
import webbrowser
from bs4 import BeautifulSoup as bs
import urllib.request
import json
import mysql.connector
import re
import time
import sys

cnx = mysql.connector.connect(user='root',
                              password='London!2019',
                              host='localhost',
                              database='dulcisinfundo_database')
cursor = cnx.cursor()

def get_recipes_data(page):
    raw_soup = urllib.request.urlopen(page).read().decode("utf8")
    time.sleep(5)
    soup = bs(raw_soup, "html.parser")
    i=0
    for article in soup.find_all('article'):
        # if div.get('class') != None:
        #     if div.attrs['class'] == ['gz-image-recipe', 'gz-video']:#
                recipe_page_soup = bs(urllib.request.urlopen(article.a.attrs['href']).read().decode("utf8"), "html.parser")
                time.sleep(3)
                for script in recipe_page_soup.find_all('script'):
                    if script.get('type') != None:
                        if script.attrs['type'] == 'application/ld+json':
                            json_text = json.loads(script.string)
                            json_keys = json_text.keys()
                            keys = []
                            for key in json_keys:
                                key = key.replace('@', '')
                                keys.append(key)
                            json_values = json_text.values()
                            values = []
                            for value in json_values:
                                if type(value) is list or type(value) is dict:
                                    value = str(value)
                                    value = value.replace('\'', '\\\'')
                                    value = value.replace('\"', '\\\"')
                                    values.append(value)
                                else:
                                    value = str(value)
                                    value = value.replace('\'', '\\\'')
                                    value = value.replace('\"', '\\\"')
                                    values.append(value)

                            #IMPORT JSON_DATA TO DATABASE
                            # text_file = open( r'C:\Users\Pats\Desktop\My Python Programs\Work in progress\Webscrape\Data extracted\raw_data.txt', 'w')
                            # text_file.write(str(json_text))
                            # text_file.write('\n\n')
                            # text_file.close()

                            # regex = re.compile(r'\"name\":\"(.*?)\",\"author\":')
                            # recipe_name = re.findall(regex, str(json_text))
                            #
                            # text_file = open( r'C:\Users\Pats\Desktop\My Python Programs\Work in progress\Webscrape\Data extracted\recipe_names.txt', 'w')
                            # text_file.write(','.join(recipe_name)+'\n\n')
                            # text_file.close()
                            # print(str(recipe_name))
                            try:
                                cursor.execute("INSERT INTO recipes_data ("+", ".join(keys)+")"
                                                "VALUES (\""+"\", \"".join(values)+"\");")
                                cnx.commit()
                                time.sleep(2)
                                i+=1
                                print(i)
                            except mysql.connector.errors.ProgrammingError as e:
                                e = str(e)
                                regex=re.compile(r'\'(.*?)\' in')
                                new_column = re.findall(regex, e)
                                cursor.execute("ALTER TABLE recipes_data "
                                                "ADD "+str(new_column[0])+" varchar(500);")
                                cnx.commit()
                                time.sleep(3)

main_page='https://www.giallozafferano.it/ricette-cat/page1/Dolci-e-Desserts/'
raw_soup=urllib.request.urlopen(main_page).read().decode('utf8')
soup=bs(raw_soup,'html.parser')
for span in soup.find_all('span'):
    if span.get('class') != None:
        if span.attrs['class'] == ['disabled', 'total-pages']:
            total_pages = span.string
i=1
for x in range(int(total_pages)):
    if i == 1:
        # regex=re.compile(r'/page(.*?)/')
        # page=regex.sub('/', main_page)
        # print('___________START___________\n'+page)
        # get_recipes_data(page)
        # print('___________END___________\n')
        i+=1
    if i > 70:
        regex=re.compile(r'/page(.*?)/')
        page=regex.sub('/page'+str(i)+'/', main_page)
        print('___________START___________\n'+page)
        get_recipes_data(page)
        print('___________END___________\n')
        i+=1

    else:
        # regex=re.compile(r'/page(.*?)/')
        # page=regex.sub('/page'+str(i)+'/', main_page)
        # print('___________START___________\n'+page)
        # get_recipes_data(page)
        # print('___________END___________\n')
        i+=1
