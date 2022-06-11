import requests
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import time
from requests_html import HTML
from requests_html import HTMLSession
from itertools import cycle
import traceback

UseProxy=False
UseDelay=False
proxies = ['103.149.162.194:80', '38.94.111.208:80', '88.99.10.250:1080', '27.64.17.187:4203', '80.48.119.28:8080']

def get_source(url):
    
    if UseProxy:
        done=False
        while done==False:
            
            proxy_pool = cycle(proxies)
            for p in range(1,11):
                #Get a proxy from the pool
                proxy = next(proxy_pool)
                
                try:
                    session = HTMLSession()
                    session.proxies = {
                                "http": proxy,
                                "https": proxy,
                                }
                    response = session.get(url)
                    response.raise_for_status() # if response is successfull, no exception will be raised
                    done=True
                    
                    return response
                    
                
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
            session = HTMLSession()        
            response = session.get(url)
            response.raise_for_status() # if response is successfull, no exception will be raised        
            return response
                            
        except requests.exceptions.RequestException as e:
            print(e)
                                
        except requests.exceptions.HTTPError as err:
            print(err)
                   
        
    

def scrape_google(query):

     
    query = urllib.parse.quote_plus(query)
    
   
    response = get_source("https://www.google.com/search?q=" + query + "&num=100")
    links = list(response.html.absolute_links)
    
        
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
    
    
    return links
    
def MainProcess():
    
    output_data=[]
    input_user = pd.read_csv('keyword_example.csv')
    c = len(input_user)
    i=0
    while i<3:
        
        results=scrape_google(str(input_user.iloc[i,0]))
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
                response = requests.get(str(links.iloc[i1,0]), timeout=60)
                response.raise_for_status() # if response is successfull, no exception will be raised
                bsh = BeautifulSoup(response.content, 'html.parser')
                marker=bsh.find(class_='entry-content')
                
                if "wp-content" in response.text and marker:
                    wpsites.append([links.iloc[i1,0]])
                    wp=wp+1
                    
                
                if wp>9:
                    break    
            except requests.exceptions.RequestException as e:
                xxx=1
                #print(e)
                                
            except requests.exceptions.HTTPError as err:
                xxx=1
                #print(err)
                
            
            
            i1=i1+1
        
        df1 = pd.DataFrame(wpsites, columns=['WPsites']) 
        df1.to_csv('wpsites.csv', index=False)
        
        os.remove('Links.csv')
        
        # get data from WP websites
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
            PH1=[]
            PH2=[]
            PH3=[]
            try:
                html = requests.get(str(wps.iloc[i2,0]))
                html.raise_for_status() # if response is successfull, no exception will be raised
                bsh = BeautifulSoup(html.content, 'html.parser')
                
                
                #H1
                x=re.findall('<h.*>(.*)</h1>', str(bsh.h1))
                try:
                    H1.append(x[0])
                except:
                    H1.append(" ")
                
                marker=bsh.find(class_='entry-content')
        
                h=1
               
                # rest of H & P
                for line in marker:
                    
                    
                    
                    if str(line).startswith('<h') and h==3:
                        h=4
                        
                        break
                    
                    if str(line).startswith('<p>') and h==3:
                        
                        temp=str(re.findall('<p>(.*)</p>', str(line)))
                        temp1=temp.replace('<span class="highlight"><em>','')
                        temp2=temp1.replace('</em>','')
                        temp3=temp2.replace('<em>','')
                        temp4=temp3.replace('</span>','')
                        temp5=temp4.replace('\xa0','')
                        temp6=temp5.replace('<strong>','')
                        temp7=temp6.replace('</strong>','')
                        
                        PH3.append(temp7)
                    
                    
                    if str(line).startswith('<h') and h==2:
                        h=3
                        
                        temp=str(re.findall('<h.*?>(.*)</h.*>', str(line)))
                        temp1=temp.replace('<span id="','')
                        temp2=temp1.replace('</span>','')
                        temp3=temp2.replace('<strong>','')
                        temp4=temp3.replace('</strong>','')
                        temp5=temp4.replace('<span class="ez-toc-section" id="','')
                        temp6=temp5.replace('<span class="ez-toc-section-end">','')
                        
                        H3.append(temp6)
                        
                    if str(line).startswith('<p>') and h==2:
                        
                        temp=str(re.findall('<p>(.*)</p>', str(line)))
                        temp1=temp.replace('<span class="highlight"><em>','')
                        temp2=temp1.replace('</em>','')
                        temp3=temp2.replace('<em>','')
                        temp4=temp3.replace('</span>','')
                        temp5=temp4.replace('\xa0','')
                        temp6=temp5.replace('<strong>','')
                        temp7=temp6.replace('</strong>','')
                        
                        PH2.append(temp7)        
                    
                    if str(line).startswith('<h') and h==1:
                        h=2
                       
                        temp=str(re.findall('<h.*?>(.*)</h.*>', str(line)))
                        temp1=temp.replace('<span id="','')
                        temp2=temp1.replace('</span>','')
                        temp3=temp2.replace('<strong>','')
                        temp4=temp3.replace('</strong>','')
                        temp5=temp4.replace('<span class="ez-toc-section" id="','')
                        temp6=temp5.replace('<span class="ez-toc-section-end">','')
                        
                        H2.append(temp6)
                    
                    if str(line).startswith('<p>') and h==1:
                        
                        temp=str(re.findall('<p>(.*)</p>', str(line)))
                        temp1=temp.replace('<span class="highlight"><em>','')
                        temp2=temp1.replace('</em>','')
                        temp3=temp2.replace('<em>','')
                        temp4=temp3.replace('</span>','')
                        temp5=temp4.replace('\xa0','')
                        temp6=temp5.replace('<strong>','')
                        temp7=temp6.replace('</strong>','')
                        
                        PH1.append(temp7)
                
                PH1_final.append("\n".join(PH1))
                PH2_final.append("\n".join(PH2))
                PH3_final.append("\n".join(PH3))
                
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
            
                  
            i2=i2+1
        
            
        try:
            output_data.append([str(input_user.iloc[i,0]),H1[0],PH1_final[0],H2[0],PH2_final[0],H3[0],PH3_final[0],H1[1],PH1_final[1],H2[1],PH2_final[1],H3[1],PH3_final[1],H1[2],PH1_final[2],H2[2],PH2_final[2],H3[2],PH3_final[2],H1[3],PH1_final[3],H2[3],PH2_final[3],H3[3],PH3_final[3],H1[4],PH1_final[4],H2[4],PH2_final[4],H3[4],PH3_final[4],H1[5],PH1_final[5],H2[5],PH2_final[5],H3[5],PH3_final[5],H1[6],PH1_final[6],H2[6],PH2_final[6],H3[6],PH3_final[6],H1[7],PH1_final[7],H2[7],PH2_final[7],H3[7],PH3_final[7],H1[8],PH1_final[8],H2[8],PH2_final[8],H3[8],PH3_final[8],H1[9],PH1_final[9],H2[9],PH2_final[9],H3[9],PH3_final[9]])
        except:
            output_data.append([str(input_user.iloc[i,0])," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "])
              
        
        os.remove('wpsites.csv')
        # loop to the next keyword
        i=i+1
        if UseDelay:
            time.sleep(60) # sleep 60 seconds
    df_output = pd.DataFrame(output_data, columns=['keyword','Top1 H1','Top1 Paragraph after H1','Top1 H2','Top1 Paragraph after H2','Top1 H3','Top1 Paragraph after H3','Top2 H1','Top2 Paragraph after H1','Top2 H2','Top2 Paragraph after H2','Top2 H3','Top2 Paragraph after H3','Top3 H1','Top3 Paragraph after H1','Top3 H2','Top3 Paragraph after H2','Top3 H3','Top3 Paragraph after H3','Top4 H1','Top4 Paragraph after H1','Top4 H2','Top4 Paragraph after H2','Top4 H3','Top4 Paragraph after H3','Top5 H1','Top5 Paragraph after H1','Top5 H2','Top5 Paragraph after H2','Top5 H3','Top5 Paragraph after H3','Top6 H1','Top6 Paragraph after H1','Top6 H2','Top6 Paragraph after H2','Top6 H3','Top6 Paragraph after H3','Top7 H1','Top7 Paragraph after H1','Top7 H2','Top7 Paragraph after H2','Top7 H3','Top7 Paragraph after H3','Top8 H1','Top8 Paragraph after H1','Top8 H2','Top8 Paragraph after H2','Top8 H3','Top8 Paragraph after H3','Top9 H1','Top9 Paragraph after H1','Top9 H2','Top9 Paragraph after H2','Top9 H3','Top9 Paragraph after H3','Top10 H1','Top10 Paragraph after H1','Top10 H2','Top10 Paragraph after H2','Top10 H3','Top10 Paragraph after H3'])
    df_output.to_csv('Output.csv', index=False) 

MainProcess()

