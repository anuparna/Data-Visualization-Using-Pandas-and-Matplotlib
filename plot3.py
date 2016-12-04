import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from pylab import rcParams
import pymysql
import pprint

# Param to update the width,height of the figure produced
rcParams['figure.figsize'] = 30, 8

"""
Yield successive n-sized chunks from l.
@Param : l - list
	 n - size of chunk
@Return: list splits

"""
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]



#Open connection to PhpMyAdmin
connection = pymysql.connect(host="localhost",            
                             user="banerjee_a",             
                             passwd="ab59958",   
                             db="banerjee_a_world_economy_database", 
                             autocommit=True,             
                             cursorclass=pymysql.cursors.DictCursor) 
cursor = connection.cursor() 

#collect agricultural employment ratios for the year 2000
sql_employment_ratios='''
   SELECT country as country,percentage_sector_employment as percentage_sector_employment FROM employment_sector_measures  
   WHERE gender='FE' and year=2000 and sector='AGR'
'''
cursor.execute(sql_employment_ratios)
agr_result=cursor.fetchall()

#collect service employment ratios for the year 2000
sql_srv_employment_ratios='''
   SELECT country as country,percentage_sector_employment as percentage_sector_employment FROM employment_sector_measures  
   WHERE gender='FE' and year=2000 and sector='SRV'
'''
cursor.execute(sql_srv_employment_ratios)
srv_result=cursor.fetchall()

#collect industry employment ratios for the year 2000
sql_ind_employment_ratios='''
   SELECT country as country,percentage_sector_employment as percentage_sector_employment FROM employment_sector_measures  
   WHERE gender='FE' and year=2000 and sector='IND'
'''
cursor.execute(sql_ind_employment_ratios)
ind_result=cursor.fetchall()

# accumulate results to map to one key
# country : 'ABC','DEF',...
resultset={}
resultset_srv={}
resultset_ind={}
for row in agr_result:    
    for column_header,column_value in row.items():
        resultset.setdefault(column_header,[]).append(column_value)
for row in srv_result:    
    for column_header,column_value in row.items():
        resultset_srv.setdefault(column_header,[]).append(column_value)
for row in ind_result:    
    for column_header,column_value in row.items():
        resultset_ind.setdefault(column_header,[]).append(column_value)

# split list into chunks of 40 countries to make plots presentable
sector_split = (list(chunks(resultset['percentage_sector_employment'], 40)))
srv_split=(list(chunks(resultset_srv['percentage_sector_employment'], 40)))
ind_split=(list(chunks(resultset_ind['percentage_sector_employment'], 40)))
country_split = (list(chunks(resultset['country'], 40)))

# plot results
for row_num in xrange(len(sector_split)): 
    
    data = {'employment in Agriculture' : pd.Series(sector_split[row_num], index=country_split[row_num]),
            'employment in Service' : pd.Series(srv_split[row_num], index=country_split[row_num]),
            'employment in Industry' : pd.Series(ind_split[row_num], index=country_split[row_num])}
    df = pd.DataFrame(data)
   
    df=df.astype(float)
    fig, axes = plt.subplots(nrows=1, ncols=1) 
        
    df['employment in Agriculture'].plot(kind='bar', ax=axes,legend=True, title='females with respect to sector : 2000 - figure '+str(row_num) , position=0,width=0.25)
    df['employment in Service'].plot(kind='bar', ax=axes,legend=True,color='red', title='females with respect to sector : 2000 - figure '+str(row_num) , position=1,width=0.25)
    df['employment in Industry'].plot(kind='bar', ax=axes,legend=True,color='green', title='females with respect to sector : 2000 - figure '+str(row_num) , position=2,width=0.25)
    
    for p in axes.patches:
	axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.savefig('figures/sector_vs_females/sector_2000_'+str(row_num)+'.png', bbox_inches='tight')
    