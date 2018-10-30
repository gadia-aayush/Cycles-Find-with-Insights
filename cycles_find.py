#!/usr/bin/env python3


##----------------------------------------------------------------------------
#---------------- CYCLES FIND WITH INSIGHTS WITHOUT PROFILING ----------------
#VERSION        : 1
##----------------------------------------------------------------------------


# Importing Libraries
import pandas as pd
from statistics import *
from datetime import datetime
import numpy as np
import json
import sys


output_passed= {}


try: #File_Input
    file_path= str(sys.argv[1])
    df= pd.read_csv(file_path)
    
    
    try: #Datetime Conversion
        recorded_data= df.iloc[0:,1].tolist()
        df.iloc[0:,0]= pd.to_datetime(df.iloc[0:,0], dayfirst=True)
        timestamp= df.iloc[0:,0].dt.strftime("%d-%m-%Y %H:%M").tolist()
        ref_time= []
        for time_val in timestamp:
            ref_time.append(time_val.split(" ")[0])
            
        
        try: #Computation Block
            
            try: #Off_Value Input
                input_data= sys.argv[2]
                input_json= json.loads(input_data)  
                off_val= np.float(input_json["input"])
                
            except: #Off-Value Input: Error Handling
                off_val = 0  #default values  
                

            # Using Enumerate Function for zero_st & zero_et
            def length_find(lst, a):
                result = []
                for i, x in enumerate(lst):
                    if (x==a):
                        result.append(i)
                return len(result)
            
            
            # Calculating no. of entries in a Day
            x=datetime.strptime(timestamp[0],'%d-%m-%Y %H:%M')
            y=datetime.strptime(timestamp[1],'%d-%m-%Y %H:%M')
            day_entries= int((3600/(y-x).total_seconds())*24) #1 day selecting
            
            
            #------------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------------
                        
            
            # Applying the logic which was applied on each day previously, to the entire dataset now
                 
            # recorded_data's dictionary create
            i=0
            data_dict= {}
            for data in recorded_data:
               data_dict[i]= data
               i+=1           
                   
                   
            # sorting data's which are less than the off-value
            off_list = [data for data in recorded_data if (data <= off_val)]
                
            
            # converting a dictionary into tuple | creating val_dict | creating r_index & f_index
            # finding no. of cycles for a particular off-value
            data_tuple= data_dict.items()
            
            r_index= []
            f_index= []
            val_dict={}
            len_cycle= []
            interval_cycle=[]
            output_data= []
            energy_use= []
            time_index= []
            peak_stats= []
                    
                   
            # to combat repeating values which exists in a dataset. [Eg: 32.58 existing at indices- 5, 18, 55 etc]
            # this is so that correct indices is fed despite of values being in repeatition.
            for value in off_list:
                rep_index= []
                for tupl in data_tuple:
                    if (value==tupl[1] ):
                        rep_index.append(tupl[0])               
                    val_dict[value]=rep_index
                        
                        
            # constructing f_index    
            for value in off_list:
                r_index.append(val_dict[value][0])
                val_dict[value].remove(val_dict[value][0])      
            
            if(len(r_index) != 0):
                for i in range(len(r_index)-1):
                    if((r_index[i+1]-r_index[i]) != 1):
                        f_index.append((r_index[i]+1, r_index[i+1]-1))            
            else:
                f_index= []
                    
                    
            # constructing array of :: cycles duration & interval b/w cycles 
            if ((len(f_index) > 1)):
                for index in range(len(f_index)-1):
                    len_cycle.append(f_index[index][1]-f_index[index][0]+1)
                    interval_cycle.append(f_index[index+1][0]-f_index[index][1]-1)  #-1 as both the points are not included 
                len_cycle.append((f_index[-1][1]-f_index[-1][0])+1)  #+1 as both the points are included          
            
            elif (len(f_index) == 1):
                len_cycle.append(f_index[0][1]-f_index[0][0]+1)
                interval_cycle.append(0)
            
            else:
                len_cycle.append(0)
                interval_cycle.append(0)
                    
                    
            # inserting- energy consumption, start end time, standard deviation & peak max, min & difference
            for each in f_index:
                sample= []
                time_index.append((timestamp[each[0]], timestamp[each[1]]))
                for point in recorded_data[each[0]: each[1]+1]:
                    sample.append(point)
                sample= np.array(sample)
                energy_use.append(np.sum(sample))
                peak_stats.append((np.max(sample), np.min(sample), np.median(sample)))
                
            
            #cycle status at data's starting & ending point
            cycle_status= []
            
            #for staring point
            try:
                if ((recorded_data[0] > off_val) and (0 not in f_index[0])):
                    cycle_status.append(1)
                else:
                    cycle_status.append(2)
            except:
                if (recorded_data[0] > off_val):
                    cycle_status.append(1)
                else:
                    cycle_status.append(2)
            
            #for ending point
            try: 
                if ((recorded_data[-1] > off_val) and (len(df)-1 not in f_index[-1])):
                    cycle_status.append(5)
                else:
                    cycle_status.append(6)
            except:
                if (recorded_data[-1] > off_val):
                    cycle_status.append(5)
                else:
                    cycle_status.append(6)
    
                    
            # inserting the output in output dictionary
            interval_cycle.append(0)
            output_data= [off_val, len(f_index), f_index, time_index, len_cycle, peak_stats, energy_use, interval_cycle] 
            output_data[4] = np.array(output_data[4])  #cycle_duration    
            output_data[-2]= np.array(output_data[-2]) #energy_consumption
            
                    
            #------------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------------
               
            
            overview= {}
            insights= {}
            
            if (len(f_index) != 0) :
                # Overview of all the Cycles
                overview["Total_No_of_Cycles"] = output_data[1]
                overview["Total_Energy_Consumption_in_kw"] = np.sum(output_data[-2])
                overview["Total_Duration_in_mins"] =  np.sum(output_data[4])*(1440/day_entries)
                overview["Maximum_Duration_in_mins"] =  np.max(output_data[4])*(1440/day_entries)
                overview["Comment_1"]= cycle_status[0]
                overview["Comment_2"]= cycle_status[1]
                
                                    
                # Detailed Insights of Cycles
                for cycle_no in range(output_data[1]):
                    insights[cycle_no+1]={}
                    insights[cycle_no+1]["Energy_Consumtion_in_kw"] = round(output_data[-2][cycle_no],2)
                    insights[cycle_no+1]["Start_Time"] = output_data[3][cycle_no][0]
                    insights[cycle_no+1]["End_Time"] = output_data[3][cycle_no][1]
                    insights[cycle_no+1]["Duration_in_mins"] = output_data[4][cycle_no]*(1440/day_entries)
                    insights[cycle_no+1]["Maximum_Value_in_kw"] = output_data[-3][cycle_no][0]
                    insights[cycle_no+1]["Minimum_Value_in_kw"] = output_data[-3][cycle_no][1]
                    insights[cycle_no+1]["Median_Value_in_kw"] = output_data[-3][cycle_no][-1]
                    insights[cycle_no+1]["Next_Cycle_After_in_mins"] = output_data[-1][cycle_no]*(1440/day_entries)

                    
            else:
                bool_output= np.array(np.array(recorded_data) >= off_val)
                true_count= np.sum(bool_output)
                if (true_count == 0):
                    overview["Total_No_of_Cycles"] = 0
                    overview["Total_Energy_Consumption_in_kw"] = 0 
                    overview["Total_Duration_in_mins"] = 0
                    overview["Maximum_Duration_in_mins"] = 0
                    overview["Comment_1"]= cycle_status[0]
                    overview["Comment_2"]= cycle_status[1]                                        
                    overview["Comment_3"]= 3              
                    
                                    
                elif (true_count == len(df)):
                    overview["Total_No_of_Cycles"] = 0
                    overview["Total_Energy_Consumption_in_kw"] = np.sum(np.array(recorded_data))
                    overview["Total_Duration_in_mins"] = len(df)*(1440/day_entries)
                    overview["Maximum_Duration_in_mins"] = len(df)*(1440/day_entries)
                    overview["Comment_1"]= cycle_status[0]
                    overview["Comment_2"]= cycle_status[1]                                        
                    overview["Comment_3"]= 4            
        
                               
                else:
                    overview["Comment"] = "Contact Data Analyst by sending the Off- Value you entered."
                    

            output_passed["status"]= "success"
            output_passed["message"]= ""
            output_passed["data"]= {"Overview" : overview , "Insights" : insights}
            output_passed["code"]= 200                
            
                                                
        except: #Computation Block: Error Handling
            output_passed["status"]= "error"
            output_passed["message"]= "Computation Error. Change Off-Value and Retry."
            output_passed["data"]= ""
            output_passed["code"]= 401    
            
        
    except: #Datetime Conversion: Error Handling
        output_passed["status"]= "error"
        output_passed["message"]= "Timestamp Values are not in DD-MM-YYYY HH:MM format in the CSV"
        output_passed["data"]= ""
        output_passed["code"]= 401      
        

except: #File Input: Error Handling
    output_passed["status"]= "error"
    output_passed["message"]= "please provide the csv file path or check the file name entered"
    output_passed["data"]= ""
    output_passed["code"]= 401


# Very Important Line
output_json = json.dumps(output_passed, ensure_ascii = 'False')
print(output_json)




 #-----------------------------
 #|| written by AAYUSH GADIA ||
 #----------------------------
 