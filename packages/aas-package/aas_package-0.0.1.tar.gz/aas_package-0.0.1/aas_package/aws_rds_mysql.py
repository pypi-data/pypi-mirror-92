# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:57:59 2020

@author: Admin
"""

"""
Install Microsoft ODBC driver for SQL
> cd C:\Python27\Scripts  
> pip install pyodbc 
"""

import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(),verbose=True,override=True)

#import pyodbc 
import mysql.connector
import datetime

server = os.getenv("SQL_SERVER")#+","+os.getenv("SQL_PORT")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")
#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30')
conn = mysql.connector.connect(
        host = server,
        database = database,
        user = username,
        password = password)

print(conn)
def sql_sync_users(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync users to sql <<<<")
    
    for mylist in mylists:
        count = count + 1

        if len(sql_get_user_by_id(mylist['Entity ID'])) == 0:   
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            # sql = "INSERT INTO CRM_Users (ID, User_name, Country, User_status, Email, User_role, User_profile, Created_date, Modified_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # cursor.execute(sql,(mylist['Entity ID'],mylist['Name'],mylist['Country'],mylist['Status'],mylist['Email'],mylist['Role Name'],mylist['Profile Name'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))  
            sql = "INSERT INTO CRM_Users (ID, User_name, Country, User_status, Email, User_role, User_profile, Created_date, Modified_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(mylist['Entity ID'],mylist['Name'],mylist['Country'],mylist['Status'],mylist['Email'],mylist['Role Name'],mylist['Profile Name'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))          
        else:
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])  
            cursor = conn.cursor()
            sql = "UPDATE CRM_Users SET User_name=%s, Country=%s, User_status=%s, Email=%s, User_role=%s, User_profile=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Name'],mylist['Country'],mylist['Status'],mylist['Email'],mylist['Role Name'],mylist['Profile Name'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID']))) 
        conn.commit()
        
   
def sql_get_user_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM CRM_Users where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs     

def sql_sync_leads(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync leads to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_lead_by_id(mylist['Entity ID'])) == 0:   
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "INSERT INTO Leads (ID, ID2, First_name, Last_name, Full_name, Chinese_name, Office, Email, Email_opt_out, Phone, Date_of_birth, Gender, Currently_studying, Highest_qualification, Qualification, Local_school_ID, Campaign_ID, Owner_name, Owner_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['ID'],mylist['First Name'],mylist['Last Name'],mylist['Full Name'],mylist['Chinese Name'],mylist['Office'],mylist['Email'],sql_boolean_format(mylist['Email Opt Out']),mylist['Phone'],mylist['Date of Birth'],mylist['Gender'],mylist['Currently Studying'],mylist['Highest Qualification'],mylist['Qualification'],mylist['Local School ID'],mylist['Campaign ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else:
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])  
            cursor = conn.cursor()
            sql = "UPDATE Leads SET First_name=%s, Last_name=%s, Full_name=%s, Chinese_name=%s, Office=%s, Email=%s, Email_opt_out=%s, Phone=%s, Date_of_birth=%s, Gender=%s, Currently_studying=%s, Highest_qualification=%s, Qualification=%s, Local_school_ID=%s, Campaign_ID=%s, Owner_name=%s, Owner_ID=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['First Name'],mylist['Last Name'],mylist['Full Name'],mylist['Chinese Name'],mylist['Office'],mylist['Email'],sql_boolean_format(mylist['Email Opt Out']),mylist['Phone'],mylist['Date of Birth'],mylist['Gender'],mylist['Currently Studying'],mylist['Highest Qualification'],mylist['Qualification'],mylist['Local School ID'],mylist['Campaign ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))  
        conn.commit()
        
        sql_sync_additonal_info('Leads','Sources',mylist)
        sql_sync_additonal_info('Leads','Nationalitys',mylist)
        sql_sync_additonal_info('Leads','Interested Programs',mylist)
        sql_sync_additonal_info('Leads','Interested Countries',mylist)
        sql_sync_additonal_info('Leads','Other Qualifications',mylist)

def sql_get_lead_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Leads where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_sync_contacts(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync contacts to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_contact_by_id(mylist['Entity ID'])) == 0:   
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "INSERT INTO Contacts (ID, ID2, First_name, Last_name, Full_name, Chinese_name, Office, Email, Email_opt_out, Phone, Date_of_birth, Gender, Currently_studying, Highest_qualification, Qualification, Local_school_ID, Campaign_ID, Lead_ID, Owner_name, Owner_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['ID'],mylist['First Name'],mylist['Last Name'],mylist['Full Name'],mylist['Chinese Name'],mylist['Office'],mylist['Email'],sql_boolean_format(mylist['Email Opt Out']),mylist['Phone'],mylist['Date of Birth'],mylist['Gender'],mylist['Currently Studying'],mylist['Highest Qualification'],mylist['Qualification'],mylist['Local School ID'],mylist['Campaign ID'],mylist['Lead ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else:
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])  
            cursor = conn.cursor()
            sql = "UPDATE Contacts SET First_name=%s, Last_name=%s, Full_name=%s, Chinese_name=%s, Office=%s, Email=%s, Email_opt_out=%s, Phone=%s, Date_of_birth=%s, Gender=%s, Currently_studying=%s, Highest_qualification=%s, Qualification=%s, Local_school_ID=%s, Campaign_ID=%s, Owner_name=%s, Owner_ID=%s, Modified_date=%s WHERE ID = %s"          
            cursor.execute(sql,(mylist['First Name'],mylist['Last Name'],mylist['Full Name'],mylist['Chinese Name'],mylist['Office'],mylist['Email'],sql_boolean_format(mylist['Email Opt Out']),mylist['Phone'],mylist['Date of Birth'],mylist['Gender'],mylist['Currently Studying'],mylist['Highest Qualification'],mylist['Qualification'],mylist['Local School ID'],mylist['Campaign ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()
        
        sql_sync_additonal_info('Contacts','Sources',mylist)
        sql_sync_additonal_info('Contacts','Nationalitys',mylist)
        sql_sync_additonal_info('Contacts','Interested Programs',mylist)
        sql_sync_additonal_info('Contacts','Interested Countries',mylist)
        sql_sync_additonal_info('Leads','Other Qualifications',mylist)

def sql_get_contact_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Contacts where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_sync_additonal_info(EntityType, SourceType, mylist):

    mylists2 = denormalize_multiselect(EntityType, SourceType, mylist)
    
    if len(mylists2) == 0 :
        return

    print(">>>> Adtl info " + SourceType + " " + mylist['Entity ID'])
    
    if len(sql_get_additional_info_by_id(EntityType,mylist['Entity ID'],SourceType)) != 0:  
        sql_delete_additonal_info(EntityType,mylist['Entity ID'],SourceType)    
    
    for mylist2 in mylists2:
        #count = count + 1                     

        #print(">> INSERT : " + str(count) + "/" + str(ttlcount)+ " " + mylist['Entity Type'] + " " + mylist['Entity ID'])
        cursor = conn.cursor()
        sql = "INSERT INTO Additional_information (Entity_type, Entity_ID, Info_type, Info, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,0,'')"
        cursor.execute(sql,(mylist2['Entity Type'],mylist2['Entity ID'],mylist2['Info Type'],mylist2['Info']))

        conn.commit()
  
def sql_delete_additonal_info(input_type,input_id,input_infotype):
    #print(">> DELETE : " + str(count) + "/" + str(ttlcount)+ " " + mylist['Entity Type'] + " " + mylist['Entity ID'])
    cursor = conn.cursor()
    sql = "DELETE from Additional_information where Entity_type = %s and Entity_ID = %s and Info_type = %s"
    cursor.execute(sql,(str(input_type),str(input_id),str(input_infotype)))
    conn.commit()
    
def sql_get_additional_info_by_id(input_type,input_id,input_infotype):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Additional_information where Entity_type IN ('" + input_type + "') and Entity_ID IN (" + str(input_id) + ") and Info_type IN ('" + input_infotype + "')"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs
    
def denormalize_multiselect(EntityType, SourceType, mylist):
    outputs = []
    d = {}
    #SourceType = 'Sources'

    #sources = mylist['Sources']
    if SourceType not in mylist.keys():
        return None
    
    sources = mylist[SourceType]
    if sources is not None:
        for source in sources:
            #Not to insert if the value already exists for the source e.g. contact1068421000000153603
            if next((item for item in outputs if item["Info"] == source), None) is None:                
                d.clear()
                d['Entity Type'] = EntityType
                d['Entity ID'] = mylist['Entity ID']
                d['Info Type'] = SourceType
                d['Info'] = source
                outputs.append(d.copy())
    return outputs

def sql_sync_institutions(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return
    
    print(">>>> sync institutions to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_institution_by_id(mylist['Entity ID'])) == 0:             
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])# + " " + mylist['ID'] + " " + mylist['Name'])
            cursor = conn.cursor()
            sql = "INSERT INTO Institutions (ID, ID2, Name, Type, State, Country, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['ID'],mylist['Name'],mylist['Type'],mylist['State'],mylist['Country'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else: 
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])  
            cursor = conn.cursor()
            sql = "UPDATE Institutions SET Name=%s, Type=%s, State=%s, Country=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Name'],mylist['Type'],mylist['State'],mylist['Country'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()
    
def sql_get_institution_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Institutions where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs
    
def sql_sync_programs(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync programs to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_program_by_id(mylist['Entity ID'])) == 0: 
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])# + " " + mylist['ID'] + " " + mylist['Name'])
            cursor = conn.cursor()
            sql = "INSERT INTO Programs (ID, ID2, Name, Type, Country, Institution_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['ID'],mylist['Name'],mylist['Type'],mylist['Country'],mylist['Institution ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else: 
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "UPDATE Programs SET Name=%s, Type=%s, Country=%s, Institution_ID=%s, Created_date=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Name'],mylist['Type'],mylist['Country'],mylist['Institution ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()
    
def sql_get_program_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Programs where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs
    
def sql_sync_applications(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync applications to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_application_by_id(mylist['Entity ID'])) == 0:            
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])# + " " + mylist['ID'] + " " + mylist['Name'])
            cursor = conn.cursor()
            sql = "INSERT INTO Applications (ID, ID2, Name, Office, Closing_date, Stage, Contact_ID, Sales_cycle_duration, Overall_sales_duration, Owner_name, Owner_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['ID'],mylist['Name'],mylist['Office'],mylist['Closing Date'],mylist['Stage'],mylist['Contact ID'],mylist['Sales_Cycle_Duration'],mylist['Overall_Sales_Duration'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else: 
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "UPDATE Applications SET Name=%s, Office=%s, Closing_date=%s, Stage=%s, Contact_ID=%s, Sales_cycle_duration=%s, Overall_sales_duration=%s, Owner_name=%s, Owner_ID=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Name'],mylist['Office'],mylist['Closing Date'],mylist['Stage'],mylist['Contact ID'],mylist['Sales_Cycle_Duration'],mylist['Overall_Sales_Duration'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()
    
def sql_get_application_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Applications where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_sync_app_program(myprograms):
    
    count = 0
    ttlcount = len(myprograms) if myprograms is not None else 0
    
    if ttlcount == 0 :
        return

    for mylists in myprograms:
        if len(sql_get_app_program_by_id(mylists[0]['App ID'],0)) != 0:  
            sql_delete_app_program(mylists[0]['App ID'])
        for mylist in mylists:
            count = count + 1
            if len(sql_get_app_program_by_id(mylist['App ID'],mylist['Entity ID'])) == 0:  
                print(">>>> Add App Program : " + str(count) + "/" + str(ttlcount) + " " + mylist['App ID'] + "/" + mylist['Entity ID'])        
                cursor = conn.cursor()
                sql = "INSERT INTO Application_programs (Application_ID, Program_ID, Deleted, Deleted_date) VALUES (%s,%s,0,'')"
                cursor.execute(sql,(mylist['App ID'],mylist['Entity ID']))

                conn.commit()

def sql_get_app_program_by_id(app_id, entity_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    if entity_id == 0 :
        sql = "SELECT * FROM Application_programs where Application_ID = " + str(app_id)
    else :
        sql = "SELECT * FROM Application_programs where Application_ID = " + str(app_id) + " and Program_ID = " + str(entity_id)
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_delete_app_program(input_id):
    #print(">> DELETE : " + str(count) + "/" + str(ttlcount)+ " " + mylist['Entity Type'] + " " + mylist['Entity ID'])
    print(input_id)
    cursor = conn.cursor()
    sql = "DELETE from Application_programs where Application_ID = " + str(input_id)
    cursor.execute(sql)
    conn.commit()

def sql_sync_app_stage_history(mystagehists):
    #print(mylists)
    count = 0
    ttlcount = len(mystagehists) if mystagehists is not None else 0
    
    if ttlcount == 0 :
        return
    
    for mylists in mystagehists:
        for mylist in mylists:
            count = count + 1
            if len(sql_get_stage_history_by_id(mylist['Entity ID'])) == 0:  
                print(">>>> Add Stage History : " + str(count) + "/" + str(ttlcount) + " " + mylist['App ID'] + "/" + mylist['Entity ID'])        
                cursor = conn.cursor()
                sql = "INSERT INTO Application_stage_history (Application_ID, ID, Stage, Close_date, Probability, Modified_date, Modified_by, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,0,'')"
                cursor.execute(sql,(mylist['App ID'],mylist['Entity ID'],mylist['Stage'],sql_convert_unreasonable_date(mylist['Close Date']),mylist['Probability'],sql_datetime_format(mylist['Modified Date']),mylist['Modified By']))
        
                conn.commit()
    
def sql_get_stage_history_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Application_stage_history where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

"""
def sql_delete_stage_history(input_id):
    #print(">> DELETE : " + str(count) + "/" + str(ttlcount)+ " " + mylist['Entity Type'] + " " + mylist['Entity ID'])
    cursor = conn.cursor()
    sql = "DELETE Application_stage_history where ID IN (%s)"
    cursor.execute(sql,input_type,input_id,input_infotype)
    conn.commit()
"""

def sql_sync_campaigns(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync campaigns to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_campaign_by_id(mylist['Entity ID'])) == 0:            
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])# + " " + mylist['ID'] + " " + mylist['Name'])
            cursor = conn.cursor()
            sql = "INSERT INTO Campaigns (ID, Name, Status, Type, Start_date, End_date, Owner_name, Owner_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['Name'],mylist['Status'],mylist['Type'],mylist['Start Date'],mylist['End Date'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else: 
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "UPDATE Campaigns SET Name=%s, Status=%s, Type=%s, Start_date=%s, End_date=%s, Owner_name=%s, Owner_ID=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Name'],mylist['Status'],mylist['Type'],mylist['Start Date'],mylist['End Date'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()

def sql_get_campaign_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Campaigns where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_sync_tasks(mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return

    print(">>>> sync tasks to sql <<<<")
    
    for mylist in mylists:
        count = count + 1
        
        if len(sql_get_task_by_id(mylist['Entity ID'])) == 0:            
            print(">> INSERT : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])# + " " + mylist['ID'] + " " + mylist['Name'])
            cursor = conn.cursor()
            sql = "INSERT INTO Tasks (ID, Subject, Status, Due_date, Closed_date, Application_ID, Contact_ID, Owner_name, Owner_ID, Created_date, Modified_date, Deleted, Deleted_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,'')"
            cursor.execute(sql,(mylist['Entity ID'],mylist['Subject'],mylist['Status'],mylist['Due Date'],sql_datetime_format(mylist['Closed Date']),mylist['Application ID'],mylist['Contact ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Created Date']),sql_datetime_format(mylist['Modified Date'])))
        else: 
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
            cursor = conn.cursor()
            sql = "UPDATE Tasks SET Subject=%s, Status=%s, Due_date=%s, Closed_date=%s, Application_ID=%s, Contact_ID=%s, Owner_name=%s, Owner_ID=%s, Modified_date=%s WHERE ID = %s"
            cursor.execute(sql,(mylist['Subject'],mylist['Status'],mylist['Due Date'],sql_datetime_format(mylist['Closed Date']),mylist['Application ID'],mylist['Contact ID'],mylist['Owner'],mylist['Owner ID'],sql_datetime_format(mylist['Modified Date']), str(mylist['Entity ID'])))
        conn.commit()

def sql_get_task_by_id(input_id):
    #print(">> sql get application by id")
    #print(mylists)
    outputs = []
    cursor = conn.cursor()
    sql = "SELECT * FROM Tasks where ID IN (" + str(input_id) + ")"
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        #print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        outputs.append(str(row[0]))
        row = cursor.fetchone()
    return outputs

def sql_mark_deleted_records(mylists):
    
    if mylists is None:
     return
    
    print(">>>> MARK DELETED RECORDS ON SQL <<<<")
    for mylist in mylists:
       if mylist is not None:
           module = mylist[0]['Module']
           if module == 'Leads': sql_mark_deleted_applications('Leads',mylist)
           elif module == 'Contacts': sql_mark_deleted_applications('Contacts',mylist)
           elif module == 'Vendors': sql_mark_deleted_applications('Institutions',mylist)
           elif module == 'Products': sql_mark_deleted_applications('Programs',mylist)
           elif module == 'Deals': sql_mark_deleted_applications('Applications',mylist)
           elif module == 'Tasks': sql_mark_deleted_applications('Tasks',mylist)
           elif module == 'Campaigns': sql_mark_deleted_applications('Campaigns',mylist)
               

def sql_mark_deleted_applications(tablename, mylists):
    #print(mylists)
    count = 0
    ttlcount = len(mylists) if mylists is not None else 0
    
    if ttlcount == 0 :
        return
    
    for mylist in mylists:
        count = count + 1
        
        print(">> MARK DEL (" + tablename + ") : " + str(count) + "/" + str(ttlcount) + " " + mylist['Entity ID'])
        cursor = conn.cursor()
        sql = "UPDATE " + tablename + " SET Deleted=%s, Deleted_date=%s WHERE ID = %s"
        cursor.execute(sql,(1,sql_datetime_format(mylist['Deleted Date']),str(mylist['Entity ID'])))
        conn.commit()
        
        if tablename in ['Leads','Contacts']:
            cursor = conn.cursor()
            sql = "UPDATE Additional_information SET Deleted=%s, Deleted_date=%s WHERE Entity_type = '" + tablename + "' and Entity_ID = %s"
            cursor.execute(sql,(1,sql_datetime_format(mylist['Deleted Date']),str(mylist['Entity ID'])))
            conn.commit()
        
        if tablename in ['Application']:
            cursor = conn.cursor()
            sql = "UPDATE Application_programs SET Deleted=%s, Deleted_date=%s WHERE Application_ID = %s"
            cursor.execute(sql,(1,sql_datetime_format(mylist['Deleted Date']),str(mylist['Entity ID'])))
            conn.commit()     
            cursor = conn.cursor()
            sql = "UPDATE Application_stage_history SET Deleted=%s, Deleted_date=%s WHERE Application_ID = %s"
            cursor.execute(sql,(1,sql_datetime_format(mylist['Deleted Date']),str(mylist['Entity ID'])))
            conn.commit() 
            
            

def sql_datetime_format(timestamp):
    if timestamp is not None:
        #return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y-%m-%dT%H:%M:%S")
        sep = max(timestamp.rfind('+'), timestamp.rfind('-'))
        if sep < 0:
            return ''
        else:
            tz = timestamp[sep:]
            ymdhms = timestamp[:sep]
            tz = tz.replace(':', '')
            timestamp = ymdhms + tz
            #print(timestamp)
            return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y-%m-%dT%H:%M:%S")
    else:
        return ''
    
def sql_convert_unreasonable_date(d):        
    return d if d >= '1900-01-01' else '1900-01-02'
    
def sql_boolean_format(b):
    if b is True:
        return 1
    else:
        return 0   
    
def sql_close_conn():
    conn.close()
    print(">> sql close connection")