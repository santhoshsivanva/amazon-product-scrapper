from bs4 import BeautifulSoup
import colorama
from scrapeProcess import scrape_details
from scrapeProcess import scrape_individuals
import requests
import time
import csv


HEADERS = ({'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def main():

    # Intro
    colorama.init()
    print(colorama.Fore.RED + "\nWelcome to the Amazon Product Scraper!")
    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    print(colorama.Fore.WHITE + "Under processing, Your file will be created soon.")
    response = requests.get(url,headers=HEADERS)
    
    #503 process handled
    while response.status_code == 503:
        response = requests.get(url,headers=HEADERS)

    soup = BeautifulSoup(response.content, "lxml")

    # process1
    process1 = scrape_details(soup)

    # process2
    if process1:
        process2 = scrape_individuals(process1)
        with open('amazon_products.csv', mode='w',encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product No', 'Name', 'Price', 'Rating', 'No of reviews', 'URL', 'ASIN', 'Manufacturer'])
            print(len(process2.items()))
            for index, product_list in process2.items():
                print(index)
                writer.writerow([index, product_list[0], product_list[1], product_list[2], product_list[3], product_list[4], product_list[5], product_list[6]])
        
        print(colorama.Fore.GREEN + "Data saved to amazon_products.csv file.")

main()