# repairmyapple_parser
The telegram bot that parser data from:  
[web-site](https://repairmyapple.ru/)
  
4 categories of goods are parsed:
* IPhones
* MacBooks
* Apple Wathces
* AirPods
  
The user selects a category for parsing,  
then selects a model, enters a price,  
selects memory or diagonal and receives the goods he needs

Installing the necessary libraries:  
pip install aiogram, requests, bs4, lxml, fake-useragent, python-dotenv