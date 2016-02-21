#!/usr/bin/python3.4
from elasticsearch import Elasticsearch
import datetime
import xlwt
import re
import logging
import os
__author__ = 'Daniel Pasacrita'
__date__ = '1/7/16'


def prepare_current_date():
    """
    Prepares and returns the current date variable for later use

    :return: The date in this format: xxxx.xx(month).xx(day)
    """
    # Create the current date variable
    t = datetime.date.today()
    # These next statements will make sure the day and month are correctly formatted
    current_day = '{:02d}'.format(t.day)
    current_month = '{:02d}'.format(t.month)
    current_year = t.year
    # Now let's put the whole thing together:
    date_formatted = str(current_year)+"."+str(current_month)+"."+str(current_day)
    return date_formatted


def query_elasticsearch(date):
    """
    This is the function that actually queries elasticsearch for the 404 pages.
    It uses the date param to use the correct elasticsearch index.

    After it grabs the data, it will then strip out the URLs and place them in the correct format.

    :param date: The date in this format: xxxx.xx(month).xx(day)
    :return: A set of every 404 returned from Elasticsearch
    """
    # Grab data from elasticsearch
    es = Elasticsearch(['elasticsearch.domain.com:9200'])
    res = es.search(index="logstash-"+date, doc_type="apache", body={"query": {
            "bool": {
                "must": [
                    {"match": {"message": "404"}}
                ],
                "should": [
                    {"match": {"message": "thing"}},
                    {"match": {"message": "otherthing"}}
                ],
                "minimum_should_match": 1,
                "must_not": {"match": {"message": "thingitshouldntmatch"}}
            }
        }})
    # Transfer data into a simple list
    fours = []
    for hit in res['hits']['hits']:
        fours.append(hit["_source"])
    # Strip the URLs from the string and put https://www.crownawards.com at the beginning
    four_urls = []
    for hit2 in fours:
        try:
            found = re.search('GET\s(.+?)\sHTTP', str(hit2)).group(1)
        except AttributeError:
            found = ''
        found = "https://www.url.com" + found
        four_urls.append(found)
    # Convert the list to a set, so URLs will be unique
    four_urls_unique = set(four_urls)
    return four_urls_unique


def output_to_text_file(four_urls_unique):
    """
    This will take the four_urls_unique param and output it to a simple text file.
    This was replaced by the Excel Spreadsheet function

    :param four_urls_unique: A set of every 404 returned from Elasticsearch
    :return: N/A
    """
    # Open the text file
    f = open('urls.txt', 'w')
    for url in four_urls_unique:
        f.write(url+"\n")
    f.close()


def output_to_excel_file(four_urls_unique, directory, filedate):
    """
    This will take the four_urls_unique param and output it to an excel spreadsheet.

    :param four_urls_unique: A set of every 404 returned from Elasticsearch
    :param directory: The present working directory
    :param filedate: The date the file was created.
    :return: N/A
    """
    # Output to an excel spreadsheet
    # Create the workbook
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    # This will make the first column much larger, about 150 characters wide:
    first_col = sheet1.col(0)
    first_col.width = 256*150
    # Fill in the workbook
    i = 0
    for url in four_urls_unique:
        sheet1.write(i, 0, url)
        i += 1
    # Save the workbook
    book.save(directory+"reports/"+"urls_spreadsheet."+filedate+".xls")


if __name__ == "__main__":
    # Grab present working directory
    pwd = os.path.dirname(os.path.realpath(__file__))+"/"

    # Logging Config
    LOG_FORMAT = '%(asctime)-12s - %(levelname)s - %(message)s'
    LOG_LEVEL = logging.INFO
    LOGFILE = pwd+"404grab.log"
    logging.basicConfig(filename=LOGFILE, format=LOG_FORMAT, level=LOG_LEVEL)

    # Get the Date
    current_date = prepare_current_date()

    # Retrieve the 404s
    four_oh_fours = query_elasticsearch(current_date)

    # Output them to the Excel Spreadsheet
    output_to_excel_file(four_oh_fours, pwd, current_date)
