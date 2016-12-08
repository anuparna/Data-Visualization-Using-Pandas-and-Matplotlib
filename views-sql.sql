SELECT wpm.country AS country, wpm.year as year,
	  wpm.percentage_working_age_of_population AS percentage_working_age_of_population, 
	  er.percentage_employment_to_population_ratio AS percentage_employment_to_population_ratio
   FROM working_population_measures wpm, employment_ratios er
   WHERE wpm.country = er.country AND          
         wpm.gender =  'FE' AND
         wpm.year = er.year
