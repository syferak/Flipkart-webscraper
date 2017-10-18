from Scraper import Scraper
import threading
import timeit
from queue import Queue

'''
This Python program scrapes information from Flipkart
Information includes product name, price, rating
Information is than stored in csv file
For further optimization use of threading is also done to achieve faster scraping
'''
#To clock the time of execution
start_time = timeit.default_timer()

#User can specify date here :product type, max pages,
#Default I have taken mobile as product and 10 pages
queue = Queue()
item = "mobile"
MAX_PAGES = 10
Scraper(item)

#Adds links to the queue for thread to execute
def create_jobs():
    for i in range(1, MAX_PAGES + 1):
        queue.put('https://www.flipkart.com/search?as=off&as-show=on&otracker=start&page=' + str(
                i) + '&q='+ item +'&viewType=list')
    queue.join()

#Creates threads
def create_threads():
    for _ in range(8):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

#Task to be performed that is scrape information and write to csv file
def work():
    while True:
        url = queue.get()
        Scraper.scrape_pages(threading.current_thread().name,url)
        Scraper.write_to_csv()
        queue.task_done()

create_threads()
create_jobs()

#Show Execution time
elapsed = timeit.default_timer() - start_time
print(elapsed)


