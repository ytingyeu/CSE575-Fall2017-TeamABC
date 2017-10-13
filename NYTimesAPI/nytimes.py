from nytimesarticle import articleAPI
import csv
import time

# Replace your won key here
api = articleAPI('db3ffd3f04b740ec9a256d1b2c8cb6c0')

def write_to_csv(result):
    """ 
    Write the info of articles to a csv file 
    Becasue we do known when will the api key exceed the limit
    So open the csv file as 'a(ppend)'
    """

    keys = result[0].keys()    
    with open('news_data.csv', 'a') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''    
    news = []

    for i in articles['response']['docs']:

        if i['headline']['main'] == '':
            break

        else:
            dic = {}
            dic['headline'] = i['headline']['main'].encode("utf8")
            dic['date'] = i['pub_date'][0:10] # cutting time of day.
            dic['url'] = i['web_url']
            news.append(dic)

    return(news)


def get_articles(query,init_begin,init_end):
    '''
    This function accepts two dates in string (e.g.'20150721')
    and a keyword (e.g.'Amnesty International', can be blank).
    It will output the parsed articles into a csv file.
    '''

    done = False

    init_begin_year = int(init_begin) / 10000
    init_begin_mon = (int(init_begin) - init_begin_year * 10000)/100
    init_begin_day = int(init_begin) % 100
    init_end_year = int(init_end) / 10000
    init_end_mon = (int(init_end) - init_end_year * 10000)/100
    init_end_day = int(init_end) % 100

    for year in range(init_begin_year, init_end_year + 1):
        for month in range(1, 13):
            if month < 10:
                begin_mon = str(year) + '0' + str(month)
                end_mon = str(year) + '0' + str(month)
            else:
                begin_date = str(year) + str(month)
                end_date = str(year) + str(month)

            for day in range(1, 32):
                all_articles = []

                if day < 10:
                    begin_date = begin_mon + '0' + str(day)
                else:
                    begin_date = end_mon + str(day)

                # skip dates before the target begin date
                if int(begin_date) < int(init_begin):
                    continue

                end_day = day + 1

                if end_day < 10:
                    end_date = begin_mon + '0' + str(end_day)
                else:
                    end_date = end_mon + str(end_day)

                # skip dates after the target end date
                if int(end_date) > int(init_end):
                    continue

                for i in range(0, 201):  # NYT limits pager to first 200 pages
                    print 'Now querying:', begin_date, i
                    
                    # query without keywords
                    if query == '': 
                        articles = api.search(
                               fq = {'source':['Reuters','AP', 'The New York Times']},
                               begin_date = begin_date,
                               end_date = end_date,
                               sort='oldest',
                               fl = 'web_url, headline, pub_date',
                               page = str(i))
                    # query with keywords
                    else:
                        articles = api.search(q = query,
                               fq = {'source':['Reuters','AP', 'The New York Times']},
                               begin_date = begin_date,
                               end_date = end_date,
                               sort='oldest',
                               fl = 'web_url, headline, pub_date',
                               page = str(i))

                    
                    if 'message' in articles:   # this indicates API limit exceeded
                        print articles['message']                    
                        return

                    elif 'response' in articles:
                        if articles['response']['docs'] != []:
                            articles = parse_articles(articles)
                            all_articles = all_articles + articles

                        else:
                            done = True
                    else:
                        done = True

                    time.sleep(5) # delay to avoid api limitation

                    if done:
                        done = False
                        break
                write_to_csv(all_articles)    # output daily

    print "Querying End..."

def main():

    key_words = ''
    result_all = []
    begin_date = '20140110'
    end_date = '20141231'

    get_articles(key_words, begin_date, end_date)


if __name__ == '__main__':
    main()


    


