from bs4 import BeautifulSoup
import os
import re
import csv

input = 'input'
output = 'output'

def get_fields(strng):
    strng = strng.replace('using Bank Account','')
    search = re.search('(?P<type>Received|Sent|Paid|Requested)\s*(?P<amount>(₹|rs)[\d*\,\.]+\s?)\s?((to|from)\s(?P<name>.*)?)?(?P<bank_acnt>X{11}\d{4})?', strng, re.IGNORECASE)
    if search:
        payment_type = search.group('type')
        amount = search.group('amount')
        name = search.group('name') if search.group('name')!=None else ''
        bank_acnt = search.group('bank_acnt') if search.group('bank_acnt')!=None else ''
        # print(payment_type.strip(), amount.strip(), name.strip(), bank_acnt.strip())
        return(payment_type.strip(), amount.strip(), name.strip(), bank_acnt.strip())
    else:
        # print(strng)
        None

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    lst = []
    for card in soup.findAll('div', {'class':'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp'}):
        for tag in card.findAll('div', {'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'}):
            tags = tag.get_text(separator = '\n', strip = True).split('\n')
            date = tags[-1]
            fields = get_fields(tags[0])
            if fields != None:
                row = [date, *fields]
                lst.append(row)
    return lst

def main():
    for file in os.listdir(input):
        if file.endswith('.html'):
            html = open(os.path.join(input, file), 'r').read()
            res = parse(html)
            filename = file.replace('.html','.csv')
            # writing to csv file 
            fields = ['Date', 'Type', 'Amount', 'To/From', 'Account']
            with open(os.path.join(output, filename), 'w') as csvfile: 
                csvwriter = csv.writer(csvfile)                 
                csvwriter.writerow(fields)
                csvwriter.writerows(res)
main()