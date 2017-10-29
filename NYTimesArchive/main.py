import csv
from nytimesarchive import ArchiveAPI

api = ArchiveAPI('db3ffd3f04b740ec9a256d1b2c8cb6c0')

def write_to_csv(result):
    """
    Write the information of articles to a csv file.
    Becasue we do not known when will the api key exceed the limit,
    open the csv file in 'a(ppend)'
    """

    keys = result[0].keys()
    with open('news_data.csv', 'a') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)

def parse_articles(articles):
    """
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    """
    news = []

    for item in articles['response']['docs']:

        #print item['headline']

        if item['headline'] == []: # if there is no news available
            continue

        else:

            dic = {}
            dic['headline'] = item['headline']['main'].encode("utf8")
            dic['date'] = item['pub_date'][0:16]
            dic['url'] = item['web_url']
            dic['document_type'] = item['document_type']

            if item['snippet'] is None:
                dic['snippet'] = []
            else:
                dic['snippet'] = item['snippet'].encode("utf8")

            news.append(dic)

    return news


def main():
    """
    The main function takes begin/end year to query and parse articles.
    Also, print the data to a csv file monthly.
    """

    begin_year = 2014
    end_year = 2017

    for year in range(begin_year, end_year + 1):

        for month in range(1, 13):

            print "Now querying", year, month, "..."
            articles_monthly = []
            articles = parse_articles(api.query(year, month))
            articles_monthly = articles_monthly + articles
            write_to_csv(articles_monthly)

    print "Query ends."

if __name__ == '__main__':
    main()
