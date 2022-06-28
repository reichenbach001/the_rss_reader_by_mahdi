CREATE DATABASE IF NOT EXISTS rss;
USE rss;
CREATE TABLE IF NOT EXISTS 
news(id int UNSIGNED NOT NULL AUTO_INCREMENT ,
agency_id INT,news_link VARCHAR(500),news_title VARCHAR(500),
crawled_at TIMESTAMP,published TIMESTAMP,sha VARCHAR(80),PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS 
news_agency(id INT NOT NULL,name VARCHAR(50) NOT NULL,rss_link VARCHAR(500),
locked BOOLEAN DEFAULT 0,last_check TIMESTAMP DEFAULT "2022-01-01 01:01:01" ,PRIMARY KEY (id));

        INSERT IGNORE INTO news_agency(id,name,rss_link) VALUES(5,'اعتماد','https://www.etemadonline.com/feeds/');
        INSERT IGNORE INTO news_agency(id,name,rss_link) VALUES(3,'فارس نیوز','https://www.farsnews.ir/rss');
        INSERT IGNORE INTO news_agency(id,name,rss_link) VALUES(2,'مهرنیوز','https://www.mehrnews.com/rss');    
        INSERT IGNORE INTO news_agency(id,name,rss_link) VALUES(1,'خبرآنلاین','https://www.khabaronline.ir/rss');
        INSERT IGNORE INTO news_agency(id,name,rss_link) VALUES(4,'شرق','https://www.sharghdaily.com/feeds/');

