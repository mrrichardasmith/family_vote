import requests
from bs4 import BeautifulSoup
import pandas as pd

blueally_ecommerce = requests.get('https://www.blueally.com/ecommerce')

blueally_microsites = blueally_ecommerce.content

soup = BeautifulSoup(blueally_microsites, "html.parser")

# Prints the attributes of the first div and .find grabs the first attribute also.
#print(soup.div.attrs)

# Prints the string within the tag if there is one which in this case there isn't of the first div
#print(soup.div.string)

# Prints the name of the tag if a name attr is not available.
#print(soup.div.name)

#for child in soup.ul.children:
#    print(child)

#lists = soup.find_all('ul')
# I thought it should have grabbed all the lists and the itterated them all printing the line items but it
# It grabbed the first list again.
#print(lists)
#for l in lists:
#    print(l.a.string)

def mircosites(soup):
    return soup.select=={'class':'partner', 'name':'a'}  
 
links = soup.select(".partner")




