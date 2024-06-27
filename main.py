import requests
import pycountry
import streamlit as st
from datetime import datetime
import math
# from dotenv import dotenv_values
import os
from dotenv import load_dotenv

key=os.environ.get('KEY')


countries = [
    "India", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", 
    "Congo, Democratic Republic of the", "Congo, Republic of the", "Costa Rica", 
    "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", 
    "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", 
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", 
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
    "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
    "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
    "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", 
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", 
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
    "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", 
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", 
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", 
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", 
    "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", 
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", 
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", 
    "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", 
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", 
    "Zambia", "Zimbabwe"
]

st.title("Latest News")

col1, col2 = st.columns([3, 1])

with col1:
    user = st.selectbox("Select a country", options=countries)

with col2:
    category = st.radio('Choose a news category', ("technology", "politics", "sports", "business"))


start_date = st.date_input("Start Date", datetime.now().date())
end_date = st.date_input("End Date", datetime.now().date())

articles_per_page = 5
page = st.number_input("Page", min_value=1, step=1, value=1)

if user and category:
    country = pycountry.countries.get(name=user).alpha_2
   
    url=f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&from={start_date}&to={end_date}&sortBy=publishedAt&language=en&pageSize=100&apiKey={key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'articles' in data:
            articles = data['articles']
            total_pages = math.ceil(len(articles) / articles_per_page)
            start_idx = (page - 1) * articles_per_page
            end_idx = start_idx + articles_per_page
            
            st.write(f"Displaying page {page} of {total_pages}")
            
            for article in articles[start_idx:end_idx]:
                st.header(article['title'])
                st.write("Published At: ", article['publishedAt'])
                if article['author']:
                    st.write("Author: ", article['author'])
                st.write("Source: ", article['source']['name'])
                st.write("News: ", article['description'])
                if article['urlToImage']:
                    image_html = f'<a href="{article["url"]}" target="_blank"><img src="{article["urlToImage"]}" width="700"></a>'
                    st.markdown(image_html, unsafe_allow_html=True)
                else:
                    st.write("Image not available")
            
            if page > 1:
                if st.button("Previous Page"):
                    page=page-1
                    
            if page < total_pages:
                if st.button("Next Page"):
                    page=page+1
                    
        else:
            st.write("No articles found for the selected criteria.")
    else:
        st.write("Failed to fetch news articles. Please check your API key and try again.")