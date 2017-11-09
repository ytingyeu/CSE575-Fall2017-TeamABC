import csv


THIRTY_COMPANY = ['Apple', 'AmericanExpress', 'Boeing', 'Caterpillar', 'Cisco', \
    'Chevron', 'Coca-Cola', 'DuPont', 'ExxonMobil', 'GeneralElectric', 'GoldmanSachs', 'HomeDepot', \
    'IBM', 'Intel', 'JohnsonJohnson', 'JPMorgan', 'McDonalds', '3M', 'Merck', \
    'Microsoft', 'Nike', 'Pfizer', 'ProcterGamble', 'Travelers', \
    'UnitedHealth', 'UnitedTechnologies', 'Visa', 'Verizon', 'Walmart', 'Disney']

NYSE_SYMBOL = {'Apple': 'AAPL', 'AmericanExpress':'AXP', 'Boeing':'BA', 'Caterpillar':'CAT', 'Cisco':'CSCO', \
    'Chevron':'CVX', 'Coca-Cola':'KO', 'DuPont':'DD', 'ExxonMobil':'XOM', 'GeneralElectric':'GE', 'GoldmanSachs':'GS', \
    'HomeDepot':'HD', 'IBM':'IBM', 'Intel':'INTC', 'JohnsonJohnson':'JNJ', 'JPMorgan':'JPM', 'McDonalds':'MCD', '3M':'MMM', \
    'Merck':'MRK', 'Microsoft':'MSFT', 'Nike':'NKE', 'Pfizer':'PFE', 'ProcterGamble':'PG', 'Travelers':'TRV', \
    'UnitedHealth':'UNH', 'UnitedTechnologies':'UTX', 'Visa':'V', 'Verizon':'VZ', 'Walmart':'WMT', 'Disney':'DIS'}


def write_to_csv(result, company_name):
    """
    Write the information of articles to a csv file.
    """
    
    keys = result[0].keys()
    with open('NYSE_' + NYSE_SYMBOL[company_name] + '.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(result)


def main():

    for company_name in THIRTY_COMPANY:

        print 'Now merging', company_name
    
        news = []

        try:
            with open('./NYT/' + company_name + '.csv', 'rb') as csvfile:

                reader = csv.reader(csvfile)
                
                for row in reader:

                    dic = {}
                    dic['date'] = row[1][0:10]
                    dic['url'] = row[3]
                    news.append(dic)

                csvfile.close()

        except IOError :
            pass

        try:
            with open('./Guardian/' + company_name + '.csv', 'rb') as csvfile:

                reader = csv.reader(csvfile)

                for row in reader:
                    dic = {}
                    dic['date'] = row[1][0:10]
                    dic['url'] = row[0]
                    news.append(dic)

                csvfile.close()

        except IOError :
            pass

            
        try:
            with open('./Reuters/' + company_name + '.csv', 'rb') as csvfile:
                
                reader = csv.reader(csvfile)
                
                for row in reader:

                    dic = {}
                    dic['date'] = row[0]
                    dic['url'] = row[2]

                    year = row[0][0:4]
                    mon = row[0][4:6]
                    day = row[0][6:8]
                    dic['date'] = year + '-' + mon + '-' + day

                    news.append(dic)

                csvfile.close()
        
        except IOError :
            pass

        
        write_to_csv(news, company_name)


if __name__ == '__main__':
    main()





