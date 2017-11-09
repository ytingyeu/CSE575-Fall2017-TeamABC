import csv

THIRTY_COMPANY = ['Apple', 'American Express', 'Boeing', 'Caterpillar', 'Cisco', \
    'Chevron', 'Coca-Cola', 'DuPont', 'ExxonMobil', 'General Electric', 'Goldman Sachs', 'Home Depot', \
    'IBM', 'Intel', 'Johnson & Johnson', 'JPMorgan Chase', 'McDonald\'s', '3M', 'Merck', \
    'Microsoft', 'Nike', 'Pfizer', 'Procter & Gamble', 'Travelers', \
    'UnitedHealth', 'United Technologies', 'Visa', 'Verizon', 'Wal-Mart', 'Disney']

COMPANY = 'Walmart'


def write_to_csv(result):
    """
    Write the information of articles to a csv file.
    """

    keys = result[0].keys()
    with open('Walmart.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


def main():

    news = []

    with open('./csv/2014-2017.csv', 'rb') as csvfile:

        reader = csv.reader(csvfile)        

        #row struc: headline, date, document_type, snippet, url
        for row in reader:
            
            if row[2] == 'article' and '/business/' in row[4] :
                if COMPANY in row[0] or COMPANY in row[3]:
                    dic = {}
                    dic['headline'] = row[0]
                    dic['date'] = row[1]
                    dic['snippet'] = row[3]
                    dic['url'] = row[4]            
                    news.append(dic)

        write_to_csv(news)

if __name__ == '__main__':
    main()
