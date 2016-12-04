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

#collect employment ratios for the year 2000
sql_employment_ratios='''
   SELECT f.country AS country, 
	  f.percentage_working_age_of_population AS percentage_working_age_of_population, 
	  f.percentage_employment_to_population_ratio AS percentage_employment_to_population_ratio
   FROM female_employment_vs_population f   WHERE f.year =2000
'''
cursor.execute(sql_employment_ratios)
result=cursor.fetchall()

# accumulate results to map to one key
# country : 'ABC','DEF',...
resultset={}
for row in result:    
    for column_header,column_value in row.items():
        resultset.setdefault(column_header,[]).append(column_value)

# split list into chunks of 40 countries to make plots presentable
ratio_split = (list(chunks(resultset['percentage_employment_to_population_ratio'], 40)))
country_split = (list(chunks(resultset['country'], 40)))

# plot results
for row_num in xrange(len(ratio_split)):    
    data = {'females with respect to working population for the year : 2000 - figure '+str(row_num) : pd.Series(ratio_split[row_num], index=country_split[row_num])}
    df = pd.DataFrame(resultset)
    df = df.set_index(['country'])
    df=df.astype(float)
    fig, axes = plt.subplots(nrows=1, ncols=1)
    
        
    df['percentage_employment_to_population_ratio'].plot(kind='bar', ax=axes,legend=True, title='females with respect to working population for the year : 2000 - figure '+str(row_num) , position=0,width=0.25)
    df['percentage_working_age_of_population'].plot(kind='bar', color='red',legend=True, ax=axes, title='females with respect to working population for the year : 2000 - figure '+str(row_num) , position=1,width=0.25)
    #axes.legend( (rects1[0], rects2[0], rects3[0]), ('y', 'z', 'k') )
    for p in axes.patches:
	axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.savefig('figures/working_population_vs_females/working_population_2000_'+str(row_num)+'.png', bbox_inches='tight')
    