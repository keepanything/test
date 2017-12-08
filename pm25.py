#coding:utf-8

from selenium import webdriver
import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import MySQLdb
import chardet

"""database configure information"""
db_host='localhost'
db_name = 'AQI'
db_user = 'qfzhang'
db_password = 'Qfzhang!23' 
table_id = "detail-data"
file_name='file:///home/qfzhang/share/PM25.in_shanghai.html'

def insert2db(tbl_name, data):
    try:
        db = MySQLdb.connect(db_host, db_user, db_password,db_name)
        cursor = db.cursor()
        sql_str = """ insert aqi_detail_data_sh (address,AQI,PM25, PM10, CO, NO2, O3,O3_8h_dn, SO2) VALUE ("""
        sql_str += """'"""+data['address']+"""'"""+','+str(data['AQI'])+','+str(data['PM25'])+','+str(data['PM10'])+','+str(data['CO'])+','+str(data['NO2'])+','+str(data['O3'])+','+str(data['O3_8h_dn'])+','+str(data['SO2'])+')'
        #print sql_str
        db.set_character_set('utf8')
        cursor.execute(sql_str)
        db.commit()
    except:
        db.close()
    
    db.close()


file_path = os.path.abspath(file_name)

browser = webdriver.Chrome()
browser.get("http://www.pm25.in/shanghai")
#browser.get(file_name)
#print browser.title

table = browser.find_element_by_id(table_id)
table_rows = table.find_elements_by_tag_name('tr')
#print "总行数:",len(table_rows)

table_cols = table_rows[0].find_elements_by_tag_name('th')
#print "总列数:", len(table_cols)
row_head = "" 
for col in table_cols:
    row_head+=col.text+' '
#    print col.text,'\n'

#print row_head

dict = {};
for row in table_rows[1:]:
    dict.clear()
    val_str = ""
    cols = row.find_elements_by_tag_name('td')
    for col in cols:
        val_str+=col.text+' '
    #print val_str
    try:
        dict['address'] = cols[0].text
        if(cols[1].text.isdigit()):
            dict['AQI'] = int(cols[1].text)
        else:
            dict['AQI'] = -1

        if(cols[4].text.isdigit()):
            dict['PM25'] = int(cols[4].text)
        else:
            dict['PM25'] = -1

        if(cols[5].text.isdigit()):
            dict['PM10'] = int(cols[5].text)
        else:
            dict['PM10'] = -1

        try:
            dict['CO'] = float(cols[6].text)
        except:
            dict['CO'] = -1.0
        
        if(cols[7].text.isdigit()):
            dict['NO2'] = int(cols[7].text)
        else:
            dict['NO2'] = -1            
        if(cols[8].text.isdigit()):
            dict['O3'] = int(cols[8].text)
        else:
            dict['O3'] = -1
        
        if(cols[9].text.isdigit()):
            dict['O3_8h_dn'] = int(cols[9].text) 
        else:
            dict['O3_8h_dn'] = -1
        
        if(cols[10].text.isdigit()):
            dict['SO2'] = int(cols[10].text) 
        else:
            dict['SO2'] = -1
    except:
        browser.quit()
        print "generate the dictionary error"
        raise
    #print dict
    insert2db('aqi_detail_data_sh', dict) 

browser.quit()
