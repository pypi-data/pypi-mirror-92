# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 18:39:56 2020

@author: Admin
"""
import zcrmsdk
#from zcrmsdk import ZCRMRecord
#import zcrmconnection
import datetime

#zcrmconnection.ZCRMConnection()
       
def ZCRMConnection(config,refresh_token,user_identifier):
        
    zcrmsdk.ZCRMRestClient.initialize(config)

    #generate access tokents from refresh token
    oauth_client = zcrmsdk.ZohoOAuth.get_client_instance()
    refresh_token = refresh_token
    user_identifier = user_identifier
    oauth_tokens = oauth_client.generate_access_token_from_refresh_token(refresh_token,user_identifier)
    
    #print(oauth_tokens)

def get_api_users(user_type):
    try:
        imports = []
        
        if user_type == 'all':
            resp = zcrmsdk.ZCRMOrganization.get_instance().get_all_users()
        elif user_type == 'DeactiveUsers':
            resp = zcrmsdk.ZCRMOrganization.get_instance().get_all_deactive_users()
        elif user_type == 'ActiveUsers':
            resp = zcrmsdk.ZCRMOrganization.get_instance().get_all_active_users()
        print (resp.status_code)
        if resp.status_code != 200:
            return
        users = resp.data
        for user in users:
            d = {}
            d['Entity ID'] = user.id                
            d['Name'] = user.full_name
            d['Country'] = user.country
            d['Status'] = user.status
            d['Email'] = user.email
            crm_role = user.role
            if crm_role is not None:
                d['Role Name'] = crm_role.name
            crm_profile = user.profile
            if crm_profile is not None:
                d['Profile Name'] = crm_profile.name
            d['Created Date'] = user.created_time                            
            d['Modified Date'] = user.modified_time
            imports.append(d.copy()) 
        return(imports)

    except zcrmsdk.ZCRMException as ex:
        print (ex.status_code)
        print (ex.error_message)
        print (ex.error_code)
        print (ex.error_details)
        print (ex.error_content)

def api_get_leads(allrecords):
    try:
        #ttlrecord = 400#No response from crm api
        per_page = 200 #max for crm api
        page = 0#1
        cvid = 1068421000018779053 #1068421000022008057
        imports = []
        d = {}
        LoopAgain = True
        
        print(">>>> Leads <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Leads')  # module API Name     

        #while (page-1)*per_page < ttlrecord:
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            #resp = module_ins.search_records_by_criteria('(Campaign:equals:[Hotel Event] 2020 Jun Pre DSE Expo)',page,per_page) 
            #resp = module_ins.search_records_by_email('alvin.tsang@aas.com.hk')
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                d['ID'] = record_ins.get_field_value('ID')
                d['First Name'] = record_ins.get_field_value('First_Name') if 'First_Name' in record_ins_data else '' 
                d['Last Name'] = record_ins.get_field_value('Last_Name') if 'Last_Name' in record_ins_data else '' 
                d['Full Name'] = record_ins.get_field_value('Full_Name') if 'Full_Name' in record_ins_data else '' 
                d['Chinese Name'] = record_ins.get_field_value('Chinese_Name') if 'Chinese_Name' in record_ins_data else '' 
                d['Office'] = record_ins.get_field_value('Office') if 'Office' in record_ins_data else '' 
                d['Sources'] = record_ins.get_field_value('Sources') if 'Sources' in record_ins_data else ''
                d['Email'] = record_ins.get_field_value('Email') if 'Email' in record_ins_data else '' 
                d['Email Opt Out'] = record_ins.get_field_value('Email_Opt_Out') if 'Email_Opt_Out' in record_ins_data else ''  
                d['Phone'] = record_ins.get_field_value('Phone') if 'Phone' in record_ins_data else ''
                d['Date of Birth'] = record_ins.get_field_value('Date_of_Birth') if 'Date_of_Birth' in record_ins_data else ''
                d['Gender'] = record_ins.get_field_value('Gender') if 'Gender' in record_ins_data else ''
                d['Nationalitys'] = record_ins.get_field_value('Nationalitys') if 'Nationalitys' in record_ins_data else ''                
                d['Highest Qualification'] = record_ins.get_field_value('Highest_Qualification') if 'Highest_Qualification' in record_ins_data else ''
                d['Other Qualifications'] = record_ins.get_field_value('Other_Qualifications') if 'Other_Qualification' in record_ins_data else ''               
                d['Currently Studying'] = record_ins.get_field_value('Currently_Studying') if 'Currently_Studying' in record_ins_data else '' 
                d['Qualification'] = record_ins.get_field_value('Qualification') if 'Qualification' in record_ins_data  else '' 
                d['Local School ID'] = record_ins.field_data['Local_School_Name']['id'] if 'Local_School_Name' in record_ins_data else 0                  
                d['Interested Programs'] = record_ins.get_field_value('Interested_Programs') if 'Interested_Programs' in record_ins_data else ''  
                d['Interested Countries'] = record_ins.get_field_value('Interested_Countries') if 'Interested_Countries' in record_ins_data else ''  
                d['Campaign ID'] = record_ins.field_data['Campaign']['id'] if 'Campaign' in record_ins_data else 0
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())  
                
            LoopAgain = True if (len(record_ins_arr) == per_page) else False
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)
   
def api_get_contacts(allrecords):
    try:
        #ttlrecord = 6394 #No response from crm api
        per_page = 200 #max for crm api
        page = 0#1
        cvid = 1068421000018779046
        imports = []
        d = {}
        LoopAgain = True
        print(">>>> Contacts <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Contacts')  # module API Name

        #while (page-1)*per_page < ttlrecord:
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            #resp = module_ins.search_records_by_criteria('(Campaign:equals:[Hotel Event] 2020 Jun Pre DSE Expo)',page,per_page) 
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                d['ID'] = record_ins.get_field_value('ID1')
                d['First Name'] = record_ins.get_field_value('First_Name') if 'First_Name' in record_ins_data else '' 
                d['Last Name'] = record_ins.get_field_value('Last_Name') if 'Last_Name' in record_ins_data else '' 
                d['Full Name'] = record_ins.get_field_value('Full_Name') if 'Full_Name' in record_ins_data else '' 
                d['Chinese Name'] = record_ins.get_field_value('Chinese_Name') if 'Chinese_Name' in record_ins_data else '' 
                d['Office'] = record_ins.get_field_value('Office') if 'Office' in record_ins_data else '' 
                d['Sources'] = record_ins.get_field_value('Source') if 'Source' in record_ins_data else ''
                d['Email'] = record_ins.get_field_value('Email') if 'Email' in record_ins_data else '' 
                d['Email Opt Out'] = record_ins.get_field_value('Email_Opt_Out') if 'Email_Opt_Out' in record_ins_data else ''  
                d['Phone'] = record_ins.get_field_value('Phone') if 'Phone' in record_ins_data else ''
                d['Date of Birth'] = record_ins.get_field_value('Date_of_Birth') if 'Date_of_Birth' in record_ins_data else ''
                d['Gender'] = record_ins.get_field_value('Gender') if 'Gender' in record_ins_data else ''
                d['Nationalitys'] = record_ins.get_field_value('Nationality1') if 'Nationality1' in record_ins_data else ''                
                d['Currently Studying'] = record_ins.get_field_value('Current_Education_Level') if 'Current_Education_Level' in record_ins_data else '' 
                d['Highest Qualification'] = record_ins.get_field_value('Highest_Qualification') if 'Highest_Qualification' in record_ins_data else ''
                d['Other Qualifications'] = record_ins.get_field_value('Other_Qualifications') if 'Other_Qualification' in record_ins_data else '' 
                d['Qualification'] = record_ins.get_field_value('Qualification_Name') if 'Qualification_Name' in record_ins_data  else '' 
                d['Local School ID'] = record_ins.field_data['Local_School_Name']['id'] if 'Local_School_Name' in record_ins_data else 0                  
                d['Interested Programs'] = record_ins.get_field_value('Interested_Subjects') if 'Interested_Subjects' in record_ins_data else ''  
                d['Interested Countries'] = record_ins.get_field_value('Interested_Countries') if 'Interested_Countries' in record_ins_data else ''  
                d['Campaign ID'] = record_ins.field_data['Campaign']['id'] if 'Campaign' in record_ins_data else 0
                d['Lead ID'] = record_ins.get_field_value('Lead_ID') if 'Lead_ID' in record_ins_data else ''             
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy()) 
                
            LoopAgain = True if (len(record_ins_arr) == per_page) else False
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)    
    
#Denormalize multi-select
def denormalize_multiselect(EntityType, SourceType, mylists):
    outputs = []
    d = {}
    #SourceType = 'Sources'
    if mylists is not None:
        for mylist in mylists:
            #sources = mylist['Sources']
            sources = mylist[SourceType]
            if sources is not None:
                for source in sources:
                    d.clear()
                    d['Entity Type'] = EntityType
                    d['Entity ID'] = mylist['Entity ID']
                    d['Info Type'] = SourceType
                    d['Info'] = source
                    outputs.append(d.copy())
    return outputs 

def api_get_institutions(allrecords):
    try:
        #ttlrecord = 2762 #No response from crm api
        per_page = 200 #max for crm api
        page = 0#1
        cvid = 1068421000018779003
        imports = []
        d = {}
        LoopAgain = True
        
        print(">>>> Institutions <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Vendors')  # module API Name
        
        #while (page-1)*per_page < ttlrecord:  
        while LoopAgain:
            page = page + 1
            #resp = module_ins.search_records_by_criteria('(Campaign:equals:[Hotel Event] 2020 Jun Pre DSE Expo)',page,per_page) 
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:     
                #record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                d['ID'] = record_ins.get_field_value('ID')
                d['Name'] = record_ins.get_field_value('Vendor_Name')
                d['Type'] = record_ins.get_field_value('Type')
                d['State'] = record_ins.get_field_value('State') if 'State' in record_ins.field_data.keys() else ''
                d['Country'] = record_ins.get_field_value('Country')
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())
            
            LoopAgain = True if (len(record_ins_arr) == per_page) else False                
            #page = page + 1
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)

def api_get_programs(allrecords):
    try:
        #ttlrecord = 7862 #No response from crm api
        per_page = 200 #max for crm api
        page = 0#1
        cvid = 1068421000018779010
        imports = []
        d = {}
        LoopAgain = True
        
        print(">>>> Programs <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Products')  # module API Name
        
        #while (page-1)*per_page < ttlrecord:            
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            #resp = module_ins.search_records_by_criteria('(Campaign:equals:[Hotel Event] 2020 Jun Pre DSE Expo)',page,per_page) 
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                                
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                d['ID'] = record_ins.get_field_value('ID')
                d['Name'] = record_ins.get_field_value('Product_Name')
                d['Full Name'] = record_ins.get_field_value('Full_Program_Name')
                d['Type'] = record_ins.get_field_value('Product_Category')
                d['Country'] = record_ins.get_field_value('Country')
                d['Institution ID']  = record_ins.field_data['Vendor_Name']['id'] if 'Vendor_Name' in record_ins_data else 0  
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())                
            
            LoopAgain = True if (len(record_ins_arr) == per_page) else False    
            #page = page + 1
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)
    
def api_get_applications(allrecords):
    try:
        #ttlrecord = 7251 #No response from crm api
        per_page = 200 #max for crm api
        page = 0#1
        cvid = 1068421000018779017 #1068421000022008064
        imports = []
        programs = []
        stagehistory = []
        d = {}
        d2 = {}
        d3 = {}
        LoopAgain = True
        
        print(">>>> Applications <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Deals')  # module API Name
                
        #while (page-1)*per_page < ttlrecord: 
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                                
                d = {}
                d['Entity ID'] = record_ins.entity_id
                d['ID'] = record_ins.get_field_value('ID')
                d['Name'] = record_ins.get_field_value('Deal_Name')
                d['Office'] = record_ins.get_field_value('Office')
                d['Closing Date'] = record_ins.get_field_value('Closing_Date')
                d['Stage'] = record_ins.get_field_value('Stage')
                d['Contact ID']  = record_ins.field_data['Contact_Name']['id'] if 'Contact_Name' in record_ins_data else 0
                d['Sales_Cycle_Duration'] = record_ins.get_field_value('Sales_Cycle_Duration')
                d['Overall_Sales_Duration'] = record_ins.get_field_value('Overall_Sales_Duration')
                d['Visa End Date'] = record_ins.get_field_value('Visa_End_Date')
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())    
                
                ### Get App Program ###
                d2 = {}
                d2 = api_get_application_programs(d['Entity ID'])
                if d2 is not None :
                    programs.append(d2.copy())  
                
                ### Get Stage History ###
                d3 = {}
                d3 = api_get_application_stage_history(d['Entity ID'])
                stagehistory.append(d3.copy())
                
            LoopAgain = True if (len(record_ins_arr) == per_page) else False                  
            #page = page + 1
            
        return imports, programs, stagehistory    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)         
        return None, None, None

def api_get_application_programs(app_id):
    try:
        imports = []
        d = {}
        record = zcrmsdk.ZCRMRecord.get_instance('Deals', app_id)  # module API Name, entityId
        resp = record.get_relatedlist_records('Products')  # related list API Name  
        print(">> Loading app program [App ID] " + app_id + " ,status: " + str(resp.status_code))
        record_ins_arr = resp.data
        for record_ins in record_ins_arr:
            #record_ins_data = record_ins.field_data
            #print(record_ins.field_data)
                           
            d.clear()
            d['App ID'] = app_id
            d['Entity ID'] = record_ins.entity_id               
            imports.append(d.copy())  
        return imports                    
    except zcrmsdk.ZCRMException as ex:
        #print(ex.status_code)
        #print(ex.error_message)
        #print(ex.error_code)
        #print(ex.error_details)
        print(ex.error_content)
   
def api_get_application_stage_history(app_id):
    try:
        imports = []
        d = {}
        record = zcrmsdk.ZCRMRecord.get_instance('Deals', app_id)  # module API Name, entityId
        resp = record.get_relatedlist_records('Stage_History')  # related list API Name  
        print(">> Loading stage history [App ID] " + app_id + " ,status: " + str(resp.status_code))
        record_ins_arr = resp.data
        for record_ins in record_ins_arr:
            #record_ins_data = record_ins.field_data
            #print(record_ins.field_data)
                            
            d.clear()
            d['App ID'] = app_id
            d['Entity ID'] = record_ins.entity_id                
            d['Stage'] = record_ins.get_field_value('Stage')
            d['Close Date'] = record_ins.get_field_value('Close_Date') if 'Close_Date' in record_ins.field_data else ''                 
            d['Probability'] = record_ins.get_field_value('probability')
            d['Modified Date'] = record_ins.get_field_value('Last_Modified_Time')
            d['Modified By'] = record_ins.field_data['modified_by']['name']                  
            imports.append(d.copy())  
        return imports
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content)    

def api_get_campaigns(allrecords):
    try:
        per_page = 200 #max for crm api
        page = 0#1
        #cvid = 1068421000000012723 #all campaigns
        cvid = 1068421000019075060
        imports = []
        d = {}
        LoopAgain = True
        
        print(">>>> Campaigns <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance('Campaigns')  # module API Name
                
        #while (page-1)*per_page < ttlrecord: 
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                #record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                          
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                d['Name'] = record_ins.get_field_value('Campaign_Name')
                d['Status'] = record_ins.get_field_value('Status')
                d['Type'] = record_ins.get_field_value('Type')
                d['Start Date'] = record_ins.get_field_value('Start_Date') if 'Start_Date' in record_ins.field_data.keys() else ''             
                d['End Date']  = record_ins.get_field_value('End_Date') if 'End_Date' in record_ins.field_data.keys() else ''
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())                
                
            LoopAgain = True if (len(record_ins_arr) == per_page) else False                  
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content) 

def api_get_tasks(allrecords,forchecklist):
    try:
        per_page = 200 #max for crm api
        page = 0#1
        #cvid = 1068421000000012753 if forchecklist else 1068421000018868068  #all tasks   
        cvid = 1068421000019003182 if forchecklist else 1068421000018868068     
        imports = []
        d = {}
        LoopAgain = True
        
        print(">>>> Tasks <<<<")
        #module_ins = zcrmsdk.ZCRMModule.get_instance('Activities')  # module API Name
        module_ins = zcrmsdk.ZCRMModule.get_instance('Tasks')  # module API Name
                
        #while (page-1)*per_page < ttlrecord: 
        while LoopAgain:
            page = page + 1
            #print(">> Loading page " + str(page))
            if allrecords: cvid = None 
            resp = module_ins.get_records(cvid,None,None,page,per_page,None)
            print(">> Loading page " + str(page) + " ,status: " + str(resp.status_code))
            record_ins_arr = resp.data
            for record_ins in record_ins_arr:
                record_ins_data = record_ins.field_data
                #print(record_ins.field_data)
                                
                d.clear()
                d['Entity ID'] = record_ins.entity_id
                #d['ID'] = record_ins.get_field_value('ID')
                d['Subject'] = record_ins.get_field_value('Subject')
                d['Status'] = record_ins.get_field_value('Status')
                d['Due Date'] = record_ins.get_field_value('Due_Date')
                d['Closed Date'] = record_ins.get_field_value('Closed_Time')              
                d['Application ID']  = record_ins.field_data['What_Id']['id'] if 'What_Id' in record_ins_data else 0
                d['Contact ID']  = record_ins.field_data['Who_Id']['id'] if 'Who_Id' in record_ins_data else 0
                d['Short Code'] = record_ins.get_field_value('Short_Code')
                d['Owner'] = record_ins.owner.name
                d['Owner ID'] = record_ins.owner.id
                d['Created Date'] = record_ins.created_time                            
                d['Modified Date'] = record_ins.modified_time
                imports.append(d.copy())
                
            LoopAgain = True if (len(record_ins_arr) == per_page) else False                  
        return imports    
    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content) 
    
def api_get_deleted_records(module,deleted_since):
    try:
        per_page = 200 #max for crm api
        page = 0#1
        imports = []
        LoopAgain = True
        #{"if-modified-since":"2020-07-02T00:00:00+00:00"}
                
        print(">>>> DELETED RECORDS : " + module + " <<<<")
        module_ins = zcrmsdk.ZCRMModule.get_instance(module)
        
        while LoopAgain:
            page = page + 1
            resp = module_ins.get_all_deleted_records(page,per_page,{"if-modified-since": deleted_since})
            print(">> Loading page " + str(resp.info.page) + " ,status: " + str(resp.status_code))
            trash_record_ins_arr = resp.data
            for record_ins in trash_record_ins_arr:
                d = {}
                d['Module'] = module
                d['Entity ID'] = record_ins.id
                d['Deleted Date'] = record_ins.deleted_time                          
                imports.append(d.copy())   
                
            LoopAgain = True if (len(trash_record_ins_arr) == per_page) else False
        return imports 

    except zcrmsdk.ZCRMException as ex:
        #print(ex.status_code)
        #print(ex.error_message)
        #print(ex.error_code)
        #print(ex.error_details)
        print(ex.error_content)
    
def api_update_app_checklist(mylists):
    try:
        count = 0
        ttlcount = len(mylists) if mylists is not None else 0
        
        if ttlcount == 0 :
            return

        print(">>>> UPDATE APP CHECKLIST <<<<")        
        for mylist in mylists:
            count = count + 1

            record = zcrmsdk.ZCRMRecord.get_instance('Deals', mylist['Application ID'])  # module API Name
            resp = record.get()
            #print(resp.data.field_data)
            shortcode = mylist['Subject'][1:3]
            #print(shortcode, mylist['Application ID'], api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'VA':
                record.set_field_value('Visa_Submission', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'VD':
                record.set_field_value('Visa_Done', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'AA':
                record.set_field_value('Accommodation_Application', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'AD':
                record.set_field_value('Accommodation_Done', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'TA':
                record.set_field_value('Ticket_Quoted', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'TD':
                record.set_field_value('Ticket_Done', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'PA':
                record.set_field_value('Pickup_Request', api_datetime_to_date(mylist['Closed Date']))
            if shortcode == 'PD':
                record.set_field_value('Pickup_Done', api_datetime_to_date(mylist['Closed Date']))
            resp=record.update()
            print(">> UPDATE : " + str(count) + "/" + str(ttlcount) + " : [App ID] " + mylist['Application ID'] + " / " + mylist['Entity ID'] + ", status : " + str(resp.status_code)) #+ " " + mylist['Application ID'] + "status : " + resp.status_code)

    except zcrmsdk.ZCRMException as ex:
        print(ex.status_code)
        print(ex.error_message)
        print(ex.error_code)
        print(ex.error_details)
        print(ex.error_content) 
    
def api_datetime_to_date(timestamp):
    if timestamp is not None:
        #return datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y-%m-%d")
        sep = max(timestamp.rfind('+'), timestamp.rfind('-'))
        if sep < 0:
            return None
        else:
            tz = timestamp[sep:]
            ymdhms = timestamp[:sep]
            tz = tz.replace(':', '')
            timestamp = ymdhms + tz
            return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y-%m-%d")
    else:
        return None