## README- Cycles-Find-with-Insights


### **BRIEF DESCRIPTION:**

  - Basically we are given Energy Data and with the help of Off- Value we are basically finding the No. of Cycles & the Insights for each cycle without profiling it for weekday's .
  
  - The script basically takes an Off- Value as an Input (only 1 value), where the Off- Value is basically the Meter Reading or the value plotted in Y Axis. 
  
  - **The script returns the Overview as well as Insights.**
    - **Overview basically tells about** the Total No. of Cycles, Total Energy Consumption for the all the Cycles, then the Total Duration when Cycle came up, Maximum Duration of a Cycle among all the Cycles & it tells whether the Cycle was already started from previous or not & whether the Cycle Ended or not or whether it was still on at the end for a particular off- value.  
    - **Insights basically tells about** each Cycle's Total Energy Consumption, Duration for each Cycle, Start & End Time of Each Cycle, Maximum, Minimum & Median Value of Energy & Duration after which Next Cycle will be seen.

-------------------------------------------------------------------------------------------------------------------


### **PREREQUISITES:**

  - written for LINUX Server.
  - written in  Python 3.6 .
  - supporting packages required- pandas, numpy, statistics, json, sys.

-------------------------------------------------------------------------------------------------------------------


### **CLIENT-END FULFILMENTS:**

The below format must be followed for the successful running of the script:  

1. **File Path ::**
   - it must be a CSV File Path.    
   - it must be passed in the second argument of sys.argv.
   
   ----------------------------------------------------------------------------------------------------------------
   
2. **CSV File Data ::**
   - Make sure that the 1st Column is Timestamps Data.   
     **NOTE :: Timestamps should have Date portion starting with Day.**  
     
   - 2nd Column must have Energy Data in kw.   
   
   ----------------------------------------------------------------------------------------------------------------   

3. **Input String ::**

	 - Off- Value viz basically the Y- Values or the Energy Data taken as Input. 
	 - it must be passed in the third argument of sys.argv.
	 - it must be passed as JSON String.  
	 - **the JSON String, alternatively the dictionary data structure should have the following Key Names::**  
	     `a. input :: it must contain the Off- Value.	[Example :: {"input" : 5} ]`  
	     **CAUTION: The above Key Names are case-sensitive, so use exactly as written above.**

   ---------------------------------------------------------------------------------------------------------------

4. **Output String ::**
   - it is passed as a JSON String.
   - **the Overview of the entire Data & all the Insights of all the Cycles are passed in the Output.**
    - **Folowing Overview are given :**  
          - Total Number of Cycles  
          - Total Energy Consumption in kw    
          - Total Duration in mins    
          - Maximum Duration in mins    
          - Comment on Cycle Starting Nature    
          - Comment on Cycle Ending Nature    
          - Comment on whether Data above Off Value or not (not always)    

    - **Folowing Insights are given :**
          - Energy Consumption in kw  
          - Cycle Start Time  
          - Cycle End Time  
          - Cycle Duration in mins  
          - Maximum Value of Energy in kw  
          - Minimum Value of Energy in kw  
          - Median Value of Energy in kw  
          - Duration after which Next Cycle is seen in mins 

   **NOTE :: All the Overview & Insights are given as per the Off- Value entered, it changes on changing                                the Off- Value.**

   ----------------------------------------------------------------------------------------------------------------   

5. **Codebook ::**

  - Comment_1 :: Cycle was On from Previous
  - Comment_2 :: Cycle was Off from Previous					  
  - Comment_3 :: All Data Below Off- Value
  - Comment_4 :: All Data Above Off- Value
  - Comment_5 :: Cycle was On till the End
  - Comment_6 :: Cycle was Off at the End					  

-------------------------------------------------------------------------------------------------------------------	

### **OUTPUT SAMPLE:**
  -	Please refer the Output Screenshots Folder.
  

-------------------------------------------------------------------------------------------------------------------	

### **AUTHORS:**

  -	coded by AAYUSH GADIA.

   
					  
