from msilib.schema import Component
import streamlit as st
import math
from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import messagebox
from pathlib import Path
from collections import Counter
import missingno as msno
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
from plotly.subplots import make_subplots
import requests
import urllib.parse


def job2(job_name, n_of_pages):
    titles = []
    company = []
    location = []
    skill = []
    country = []
    new_location = []
    final_loc = []
    date = []
    work_hours = []
    twon = []
    city = []
    final_skill = []
    experience = []
    experience_years = []
    skill2 = []
    links = []
    job_des = []
    label = []
    education_level = []
    job_req = []
    vacancies = []
    num = 0
    job_name = job_name.lower()
    name = job_name.split(' ')
    n_of_pages = n_of_pages-1
    url = 'https://wuzzuf.net/search/jobs/?a=navbg&q=' + \
        str(name[0])+'%20'+str(name[1])+'&start='+str(num)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    page_limit = int(soup.find('strong').text)
    if(n_of_pages > page_limit//15):
        print('Sorry,Limited Pages,maximum pages you can get is ', (page_limit//15)+1)
    else:
        while True:
            if(num > n_of_pages):
                break
            job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
            company_names = soup.find_all('a', {'class': 'css-17s97q8'})
            locations = soup.find_all('span', {'class': 'css-5wys0k'})
            time = soup.find_all('div', {'class': 'css-1lh32fc'})
            skill_descr = soup.find_all('div', {'class': 'css-y4udm8'})
            posted_time = soup.find_all('div', {'class': 'css-d7j1kk'})
            for j in range(len(job_titles)):
                titles.append(job_titles[j].text)
                links.append('https://wuzzuf.net/' +
                             job_titles[j].find('a').attrs['href'])
                company.append(company_names[j].text[:-2])
                location.append(locations[j].text)
                date.append(posted_time[j].text)
                work_hours.append(time[j].text)
                skill.append(skill_descr[j].text)
                label.append(job_name)
#             print(links)
            num += 1
        for link in links:
            #             print(link)
            try:
                headers = {
                    "Connection": "keep-alive",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                }
                result2 = requests.get(link, headers=headers, timeout=5)
                src2 = result2.content
                soup2 = BeautifulSoup(src2, 'lxml')
            #     salaries=soup2.find('span',{'class':'css-4xky9y'})
                description = soup2.find(
                    "span", attrs={"itemprop": "description"})
                edu_level = soup2.find(
                    "dd", attrs={"class": "requirement-content"})
                job_r = soup2.find(
                    "span", attrs={"itemprop": "responsibilities"})
            #     print(description)
                job_des.append(description.text)
                education_level.append(edu_level.text)
                job_req.append(job_r.text)
            except:
                job_des.append('No Job Description')
                job_req.append('No Job Requirement')

        for i in range(len(location)):
            country.append(location[i].split(',')[-1])
            new_location.append(location[i].split(',')[:-1])
        for i in range(len(new_location)):
            final_loc.append(' '.join(new_location[i]))

        for i in range(len(skill)):
            skill[i] = skill[i].lstrip(work_hours[i])
            date[i] = date[i].replace(location[i], '')
            date[i] = date[i].replace(company[i], '')
        for i in range(len(date)):
            date[i] = date[i][3:]

        for i in range(len(titles)):
            skill[i].split('·')
            skill[i] = skill[i].replace('Yrs of Exp', '')
            experience.append(skill[i].split('·')[0])
            experience_years.append(skill[i].split('·')[1])
            skill2.append(skill[i].split('·')[2:])
        for i in range(len(new_location)):
            final_skill.append(' '.join(skill2[i]))
            if(len(location[i].split(',')) == 2):
                twon.append('No twon avaliable')
                city.append(location[i].split(',')[0].strip())
            else:
                twon.append(location[i].split(',')[0].strip())
                city.append(location[i].split(',')[1].strip())
        df = pd.DataFrame({'job_name': label, 'job_title': titles, 'company': company, 'town': twon, 'city': city, 'country': country, 'date': date, 'work_hours': work_hours,
                          'career_level': experience, 'experience_yreas': experience_years, 'job_description': job_des, 'job_requirement': job_req, 'skills': final_skill})
        return df

# st.title("Hallo ")
# uploaded_file = st.file_uploader('Upload your file here')
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     st.write(df)
# with st.form(key='my_form'):
#     text_input = st.text_input(label='Enter some text')
#     submit_button = st.form_submit_button(label='Submit')
# Declare a form and call methods directly on the returned object
# form = st.form(key='my_form')
# form.text_input(label='Enter some text')
# submit_button = form.form_submit_button(label='Submit')


def analysis(df, job_n):

    c1 = Counter(df[df['job_name'] == job_n.lower()]['city'])
    latitude = []
    longitude = []
    for address in c1.keys():
        url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address) + '?format=json'
        response = requests.get(url).json()
        latitude.append(response[0]["lat"])
        longitude.append(response[0]["lon"])
    values = list(c1.values())
    city_name = list(c1.keys())
    col_names = ['latitude', 'longitude', 'values', 'city']
    df_b = pd.DataFrame()
    df_b['latitude'] = latitude
    df_b['longitude'] = longitude
    df_b['values'] = values
    df_b['city_name'] = city_name
    df_b['latitude'] = df_b['latitude'].astype(float)
    df_b['longitude'] = df_b['longitude'].astype(float)
    fig = px.scatter_mapbox(df_b, lat='latitude', lon='longitude', size='values', size_max=100,
                            zoom=4.4, center=dict(lat=df_b['latitude'].mean() + 1, lon=df_b['longitude'].mean() - 1.5),
                            mapbox_style="stamen-terrain", title='{} Distribution'.format(job_name.capitalize()),
                            color='values', hover_name="city_name")
    fig.update_layout(title_x=0.5, height=800)
    fig.show()


# with st.form(key='scraping'):
st.set_page_config(page_title="Web Scarping",
                   page_icon=":teda:", layout="wide")
st.title("Web Scarping Wuzzuf")
st.write("---")
job_name = st.text_input("Enter Job Name")
page_numbers = st.number_input("Enter Number of Pages")
scrap_button = st.button(label="Scrap")
if scrap_button:
    df = job2(job_name, page_numbers)
    st.write(df)
    st.success("Success! You scraped the {} data ".format(
        job_name.capitalize()))
    st.download_button(label="Download CSV", data=df.to_csv(), mime='text/csv')
    analysis(df=df, job_n=job_name)
