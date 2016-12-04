import csv
import pymysql

# defined a map so that CSVs from different sources represent the same gender
gender_map={"MEN":"MA","WOMEN":"FE"}

# defined a map so that CSVs from different sources represent the same year
year_map={"2000":"2000 [YR2000]","2014":"2014 [YR2014]"}

#collect only percentages of working-age-population for the years 2000 and 2014 for only men and women and not the total
country_year_working_age_population_reader = open('data-source/country_year_working_age_population.csv')
country_year_working_age_population = csv.DictReader(country_year_working_age_population_reader)
pc_working_population_rows=[]
for row in country_year_working_age_population:
    if row['MEASURE'] == 'PC_WKGPOP' and (row['TIME'] in year_map.keys()) and row['SUBJECT'] != 'TOT':
        pc_working_population_rows.append(row)

working_population_rows=[]
for row in pc_working_population_rows: 
    data={}
    country=row['LOCATION'] #fetch the country
    gender=row['SUBJECT'] #fetch the gender
    
    #Fill the dict to insert into database
    data["year"]=row['TIME']
    data["country"]=country
    data["gender"]=gender_map[gender]
    data["percentage_working_age_of_population"]=row['Value']
    working_population_rows.append(data)
    


#Collect those rows which correspond the country and the gender from the 3rd CSV 
employment_ratios_reader = open('data-source/employment_to_population_ratio.csv')
employment_ratios = csv.DictReader(employment_ratios_reader)
employment_ratio_rows=[]
for employment_ratio in employment_ratios:
    if "SL.EMP.TOTL." in employment_ratio['Series Code']:        
        for year,year_format in year_map.items():
            data={}
            data["country"]=employment_ratio['Country Code']
            data["year"]=year
            data["percentage_employment_to_population_ratio"]= employment_ratio[year_format] if employment_ratio[year_format]!='..' else 0.00  
            employment_ratio_rows.append(data)
            
        
# fetch those rows which correspond the country and the gender from the 2nd CSV 
gender_sector_employment_reader = open('data-source/gender_sector_employment.csv')
gender_sector_employment = csv.DictReader(gender_sector_employment_reader)
employment_sector_rows=[]
for employment_detail in gender_sector_employment:
    code=employment_detail['Series Code']
    if code:
        split_string = code.split(".") #code is in the form of 'SL.SRV.EMPL.FE.ZS' where FE denotes gender and SRV denotes sector
        for year,year_format in year_map.items():
            data={}
            data["country"]=employment_detail['Country Code']
            data["gender"]=split_string[3]
            data["sector"]=split_string[1]
            data["year"]=year
            data["percentage_sector_employment"]=employment_detail[year_format] if employment_detail[year_format]!='..' else 0.00  
            employment_sector_rows.append(data)
                
#Database operations start here        
connection = pymysql.connect(host="localhost",            
                             user="banerjee_a",             
                             passwd="ab59958",   
                             db="banerjee_a_world_economy_database", 
                             autocommit=True,             
                             cursorclass=pymysql.cursors.DictCursor) 
cursor = connection.cursor() 
# insert into database with the values in the list
sql_working_population='''
                    INSERT INTO working_population_measures
                    (country,gender,year,percentage_working_age_of_population) 
                    VALUES
                    (%(country)s,%(gender)s,%(year)s,%(percentage_working_age_of_population)s)
                    '''
generated_working_population = [] #contains all the ids generated during the execution of the insert statement
for data in working_population_rows:
    cursor.execute(sql_working_population, data)
    generated_working_population.append(cursor.lastrowid)
    
sql_employment_ratio='''
                    INSERT INTO employment_ratios
                    (country,year,percentage_employment_to_population_ratio) 
                    VALUES
                    (%(country)s,%(year)s,%(percentage_employment_to_population_ratio)s)
                    '''
generated_employment_ratio_ids = [] #contains all the ids generated during the execution of the insert statement
for data in employment_ratio_rows:
    cursor.execute(sql_employment_ratio, data)
    generated_employment_ratio_ids.append(cursor.lastrowid)
    
sql_employment_sector='''
                    INSERT INTO employment_sector_measures
                    (country,gender,sector,year,percentage_sector_employment) 
                    VALUES
                    (%(country)s,%(gender)s,%(sector)s,%(year)s,%(percentage_sector_employment)s)
                    '''
generated_employment_sector_ids = [] #contains all the ids generated during the execution of the insert statement
for data in employment_sector_rows:
    cursor.execute(sql_employment_sector, data)
    generated_employment_sector_ids.append(cursor.lastrowid)
    
cursor.close()