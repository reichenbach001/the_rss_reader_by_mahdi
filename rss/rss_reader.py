import time
from pickle import TRUE
import feedparser as fp
import mysql.connector as mql
import datetime
import hashlib
import re
import urllib

def lock_column(table_name,the_row):
    #lock_column locks column by insertin TRUE.
    query="UPDATE {0} SET locked=1 WHERE rss_link='{1}';"
    query_final=query.format(table_name,the_row)
    print("locked row:",the_row)
    curs.execute(query_final)
    db.commit()

def unlock_column(table_name,the_row,this_moment):
    #ulock_column ulocks column by inserting FALSE and updates the last_check value.
    query='UPDATE {0} SET locked=0,last_check="{1}" WHERE rss_link="{2}";'
    query_final=query.format(table_name,this_moment,the_row)
    print("row unlocked\n")
    curs.execute(query_final)
    db.commit()



def time_differ(time1):
    #this function calculates the time difference from time1 and now and returns in minute!
    time_end_temp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    time_end=time.strptime(time_end_temp,"%Y-%m-%d %H:%M:%S")
    time_start=time.strptime(time1,"%Y-%m-%d %H:%M:%S")
    
    
    time_difference_in_minute=(time_end.tm_year-time_start.tm_year)*365*24*60+(time_end.tm_mon-time_start.tm_mon)*30*24*60+(time_end.tm_mday-time_start.tm_mday)*24*60+(time_end.tm_hour-time_start.tm_hour)*60+(time_end.tm_min-time_start.tm_min)
   
    if(time_difference_in_minute>=0):
        return(time_difference_in_minute)
    else:
        return(0)

    


def connected(host):
    try:
        urllib.request.urlopen(host)
        print("connected to:"+host)
        print("---fetching data from:"+host)
    except:
        print("couldn't connect to:"+host)



def refine_time(raw_time):
    temp_txt = raw_time.split(" ")
    temp_txt_2 = temp_txt[1]+" "+temp_txt[2]+" "+temp_txt[3]+" "+temp_txt[4]

    try:
        temp_time_struct = time.strptime(temp_txt_2, "%d %b %Y %H:%M:%S")
        refined_time = "{0}-{1}-{2} {3}:{4}:{5}"
        refined_time = refined_time.format(temp_time_struct.tm_year, temp_time_struct.tm_mon, temp_time_struct.tm_mday,
                                           temp_time_struct.tm_hour, temp_time_struct.tm_min, temp_time_struct.tm_sec)

    except:
        refined_time = "{0}-{1}-{2} {3}:{4}:{5}"
        temp_txt_2 = temp_txt[0]+" "+temp_txt[1] + \
            " "+temp_txt[2]+" "+temp_txt[3]
        temp_time_struct = time.strptime(temp_txt_2, "%d %b %Y %H:%M:%S")
        refined_time = refined_time.format(temp_time_struct.tm_year, temp_time_struct.tm_mon, temp_time_struct.tm_mday,
                                           temp_time_struct.tm_hour, temp_time_struct.tm_min, temp_time_struct.tm_sec)

    return refined_time


db = mql.connect(
    host="mysqll",
    user="root",
    password="toor"
)
if(db):
    print("connected")
else:
    print("did not connect")


curs = db.cursor()
curs.execute("USE rss;")

curs.execute("SELECT id,rss_link,last_check,locked from news_agency;")
news_agencies = curs.fetchall()



while_counter=0
while (True):
    
    for news_agency_link in news_agencies:
        is_locked=news_agency_link[3]

        last_check_temp=news_agency_link[2]
        last_check=str(last_check_temp) #this code makes a last check time in format "Y-Mo-D H:Mi:S"

        news_agency_link_str = str(news_agency_link)
        news_agency_link_refined = re.sub("[',()]", "", news_agency_link_str)
        news_agency_link_refined = news_agency_link_refined.split(" ")
        
        

        time_difference_in_min=time_differ(last_check) #calculates how much time passed since the last time that this agency's rss is crawled.

        if(is_locked!=TRUE and time_difference_in_min>30  ):# this line makes sure that the agency has two demanded condition to be crawled: 1 is not used by another machine and 2 it has been more than 30 minutes passed.
            lock_column('news_agency',news_agency_link_refined[1])
            connected(news_agency_link_refined[1])
            feed = fp.parse(news_agency_link_refined[1])
            llen = len(feed.entries)
            for i in range(llen):
                newss = feed.entries[i]
                published_time=refine_time(newss.published)

                if (published_time>last_check):# this line checks if the publish date of entry "i" is not older than last_check 
                    submit_query = 'INSERT IGNORE INTO news(agency_id,news_link,news_title,crawled_at,published,sha) VALUES ("{1}","{2}","{3}","{4}","{5}","{6}");'
                    this_moment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    a_string = newss.link+newss.title
                    news_hash = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
                    news_title_refined = re.sub('["]', '', newss.title)
                    news_link_refined = re.sub('["]', '', newss.link)
                    submit_query_final = submit_query.format(int(
                        i), news_agency_link_refined[0], news_link_refined, news_title_refined, this_moment,published_time, news_hash)
                    curs.execute(submit_query_final)
                    
                    db.commit()
                else:
                    break
            unlock_column('news_agency',news_agency_link_refined[1],this_moment)            
    
        



       
    while_counter+=1
    print("run time: ",while_counter,"\n still running...")

    curs.execute("SELECT id,rss_link,last_check,locked from news_agency;")#this line updates the last check info
    news_agencies = curs.fetchall()

    time.sleep(10)


