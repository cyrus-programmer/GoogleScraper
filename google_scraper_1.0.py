from ast import excepthandler
import requests
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import csv
import time
from requests_html import HTML
from requests_html import HTMLSession
from itertools import cycle
import cloudscraper
from zmq import proxy

sess = requests.session()
scraper = cloudscraper.create_scraper(sess)
header = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
}


UseProxy = True
UseDelay = True
proxies = [] # Add IP here
def filter_string(string):
    if '[' or ']' in string:
        string = string.replace('[', ' ')
        string = string.replace(']', ' ')
    string = string.replace("'", " ")
    string.replace('  ', ' ')
    string.replace('   ', ' ')
    string = string.strip()
    return string
def filter_html(string):
    check1 = 0
    check2 = 0
    while check1!=-1 and check2!=-1:
        if '<' and '>' in string:
            end = string.index('>')
            start = string.index('<')
            string = string.replace(string[start:end+1], ' ')
            check1 = string.find('<')
            check2 = string.find('>')
        else:
            break
    return string.strip()
def get_source(url):
    
    if UseProxy:
        done=False
        while done==False:
            
            proxy_pool = cycle(proxies)
            for p in range(1,11):
                #Get a proxy from the pool
                proxy = next(proxy_pool)
                
                try:
                    session = requests.session()
                    session = cloudscraper.create_scraper(sess = session)
                    session.proxies = {
                                "http//": proxy,
                                "https//": proxy,
                                }
                    response = session.get(url, headers=header)
                    response.raise_for_status() # if response is successfull, no exception will be raised
                    print(response.json)
                    done=True
                    
                    return response, proxy
                    
                
                except requests.exceptions.RequestException as e:
                    print(e)
                    print(" ")
                    print("retrying with new proxy")
                    
                except requests.exceptions.HTTPError as err:
                    print(err)
                    print(" ")
                    print("retrying with new proxy")    
    else:
        try:
            session = requests.session()
            session = cloudscraper.create_scraper(sess = session)
            session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
            response = session.get(url)
            response.raise_for_status() # if response is successfull, no exception will be raised   
            return response
                            
        except requests.exceptions.RequestException as e:
            print(e)
                                
        except requests.exceptions.HTTPError as err:
            print(err)
            
        except:
            pass
            
def scrape_google(query):

     
    query = urllib.parse.quote_plus(query)
    
   
    response, proxy = get_source("https://www.google.com/search?q=" + query + "&num=100")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    relative_keywords = soup.find('div', {'çlass':'y6Uyqe'})
    decks = soup.findAll('div', {'class':'AJLUJb'})
    searches = []
    for deck in decks:
        cards = deck.findAll('div')
        for card in cards:
            if card.text != '':
                searches.append(card.text)
    cards = soup.findAll('div', {'class' : 'yuRUbf'})
    links = []
    for card in cards:
        link = card.find('a')['href']
        links.append(link)
        
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://translate.google.',
                      'https://www.youtube')

    for url in links[:]:
        
        if url.startswith(google_domains):
            links.remove(url)
    
    
    return links, searches, proxy

def main():
    
    input_user = pd.read_csv('keyword_example.csv')
    c = len(input_user)
    i=0
    while i<c:
        output_data={
                'keyword' : [],
                'Top1 Link': [],
                'Top1 H1': [],
                'Top1 Paragraph after H1': [],
                'Top1 H2': [],
                'Top1 Paragraph after H2': [],
                'Top1 H3': [],
                'Top1 Paragraph after H3': [],
                'Top2 Link': [],
                'Top2 H1': [],
                'Top2 Paragraph after H1': [],
                'Top2 H2': [],
                'Top2 Paragraph after H2': [],
                'Top2 H3': [],
                'Top2 Paragraph after H3': [],
                'Top3 Link': [],
                'Top3 H1': [],
                'Top3 Paragraph after H1': [],
                'Top3 H2': [],
                'Top3 Paragraph after H2': [],
                'Top3 H3': [],
                'Top3 Paragraph after H3': [],
                'Top4 Link': [],
                'Top4 H1': [],
                'Top4 Paragraph after H1': [],
                'Top4 H2': [],
                'Top4 Paragraph after H2': [],
                'Top4 H3': [],
                'Top4 Paragraph after H3': [],
                'Top5 Link': [],
                'Top5 H1': [],
                'Top5 Paragraph after H1': [],
                'Top5 H2': [],
                'Top5 Paragraph after H2': [],
                'Top5 H3': [],
                'Top5 Paragraph after H3': [],
                'Top6 Link': [],
                'Top6 H1': [],
                'Top6 Paragraph after H1': [],
                'Top6 H2': [],
                'Top6 Paragraph after H2': [],
                'Top6 H3': [],
                'Top6 Paragraph after H3': [],
                'Top7 Link': [],
                'Top7 H1': [],
                'Top7 Paragraph after H1': [],
                'Top7 H2': [],
                'Top7 Paragraph after H2': [],
                'Top7 H3': [],
                'Top7 Paragraph after H3': [],
                'Top8 Link': [],
                'Top8 H1': [],
                'Top8 Paragraph after H1': [],
                'Top8 H2': [],
                'Top8 Paragraph after H2': [],
                'Top8 H3': [],
                'Top8 Paragraph after H3': [],
                'Top9 Link': [],
                'Top9 H1': [],
                'Top9 Paragraph after H1': [],
                'Top9 H2': [],
                'Top9 Paragraph after H2': [],
                'Top9 H3': [],
                'Top9 Paragraph after H3': [],
                'Top10 Link': [],
                'Top10 H1': [],
                'Top10 Paragraph after H1': [],
                'Top10 H2': [],
                'Top10 Paragraph after H2': [],
                'Top10 H3': [],
                'Top10 Paragraph after H3': [],
                'Relative Searches': []
            }
        
        results, relative_keywords, proxy=scrape_google(str(input_user.iloc[i,0]))
#         print(results)
        df = pd.DataFrame({'Links':results}) 
        df.to_csv('Links.csv', index=False)
        
        # detecting wordpress sites
        links = pd.read_csv('Links.csv')
        c1=len(links)
        i1=0

        wp=0
        wpsites=[]

        while i1<c1:
            try:
                response = scraper.get(str(links.iloc[i1,0]), timeout=60, proxies={"http//": proxy,"https//": proxy,})
                response.raise_for_status() # if response is successfull, no exception will be raised
                bsh = BeautifulSoup(response.content, 'html.parser')
                marker=bsh.find(class_='entry-content')
                faulty_link = 'https://www.pupbox.com/training/when-do-puppies-lose-their-baby-teeth/'
                if "wp-content" in response.text and marker:
                    if str(links.iloc[i1,0]) != faulty_link:
                        wpsites.append(str(links.iloc[i1,0]))
                        wp=wp+1

                if wp>9:
                    break    
            except requests.exceptions.RequestException as e:
                xxx=1
                # print(e)

            except requests.exceptions.HTTPError as err:
                xxx=1
                # print(err)
            except:
                pass



            i1=i1+1
        print("Wordpress site links are scraped")
        df1 = pd.DataFrame(wpsites, columns=['WPsites']) 
        df1.to_csv('wpsites.csv', index=False)
        
        os.remove('Links.csv')
        H1=[]
        PH1_final=[]
        H2=[]
        PH2_final=[]
        H3=[]
        PH3_final=[]

        i2=0
        wps = pd.read_csv('wpsites.csv')
        c2=len(wps)

        while i2<c2:
            try:
                html = scraper.get(str(wps.iloc[i2,0]), headers=header)
                html.raise_for_status() # if response is successfull, no exception will be raised
                soup = BeautifulSoup(html.content, 'html.parser')
                content = soup.find('div', {'class', 'entry-content'})
                if content == None:
                    content = soup.select('[class*=entry-content]')[0]
                try:
                    h1 = soup.find('h1', {'class', 'entry-title'})
                except:
                    try:
                        h1 = soup.find('h1')
                    except:
                        h1 = content.find('h1')
                h1 = filter_html(str(h1))
                try:
                    full_p1 = ''
                    p1 = content.findAll('p')[0:2]
                    for para in p1:
                        p1 = filter_html(str(para))
                        full_p1+=p1
                except:
                    try:
                        p1 = filter_html(str(content.find('p')))
                    except:
                        try:  
                            p1 = content.find('p').text
                        except:
                            try:
                                p1 = soup.find('p').text
                            except:
                                pass
                H1.append(h1)
                PH1_final.append(full_p1)
                tags = []
                h2_index = 0
                p2_index = 0
                h3_index = 0
                p3_index = 0
                for u in content:
                    tags.append(str(u))
                for u in range(len(tags)):
                    if tags[u].startswith('<h2') or tags[u].startswith('<h3'):
                        h2 = filter_html(tags[u])
                        h2_index = u
                        H2.append(h2)
                        break
                for u in range(h2_index+1, len(tags)):
                    full_p2 = ''
                    if tags[u].startswith('<h2') or tags[u].startswith('<h3'):
                        break
                    if tags[u].startswith('<p>'):
                        p2 = filter_html(tags[u])
                        full_p2 += p2
                        p2_index = u
                        PH2_final.append(full_p2)
                for u in range(p2_index, len(tags)):
                    if tags[u].startswith('<h2') or tags[u].startswith('<h3'):
                        h3 = filter_html(tags[u])
                        h3_index = u
                        H3.append(h3)
                        break
                for u in range(h3_index+1, len(tags)):
                    full_p3 = ''
                    if tags[u].startswith('<h2') or tags[u].startswith('<h3'):
                        break
                    if tags[u].startswith('<p>'):
                        p3 = filter_html(tags[u])
                        full_p3+=p3
                        p3_index = u
                        PH3_final.append(full_p3)

                if len(H1)<i2+1:
                    H1.append(" ")
                if len(H2)<i2+1:
                    H2.append(" ")
                if len(H3)<i2+1:
                    H3.append(" ")  

                if len(PH1_final)<i2+1:
                    PH1_final.append(" ")    

                if len(PH2_final)<i2+1:
                    PH2_final.append(" ")

                if len(PH3_final)<i2+1:
                    PH3_final.append(" ")

            except requests.exceptions.RequestException as e:
                print(e)
            except requests.exceptions.HTTPError as err:
                print(err)
            except:
                pass
            i2=i2+1
        output_data['keyword'].append(input_user['Keyword'][i])
        for k in range(c2):
            output_data[f'Top{k+1} Link'].append(wps['WPsites'][k])
            output_data[f'Top{k+1} H1'].append(H1[k])
            output_data[f'Top{k+1} Paragraph after H1'].append(PH1_final[k])
            output_data[f'Top{k+1} H2'].append(H2[k])
            output_data[f'Top{k+1} Paragraph after H2'].append(PH2_final[k])
            output_data[f'Top{k+1} H3'].append(H3[k])
            output_data[f'Top{k+1} Paragraph after H3'].append(PH3_final[k])
        keywords = ''
        for keyword in relative_keywords:
            keywords+=keyword
            keywords += ','
        output_data['Relative Searches'].append(keywords)
        
        for key in output_data:
            if len(output_data[key]) != len(output_data['Top1 Link']):
                for count in range(len(output_data['Top1 Link'])-len(output_data[key])):
                    output_data[key].append('-')
        if c2 != 10:
            for f in range(10-c2):
                for key in output_data:
                    output_data[key].append('-')
            
        
        os.remove('wpsites.csv')
        # loop to the next keyword
        
        if i==0:
            df_output = pd.DataFrame(output_data)
            df_output.to_csv('Output.csv', index=False)
        else:
            df_output = pd.DataFrame(output_data)
            df_output.to_csv('Output.csv', index=False, mode='a', header=False)
        i=i+1
        if UseDelay:
            time.sleep(30) # sleep 30 seconds
    print(f"{i} Keyword are scraped")
main()