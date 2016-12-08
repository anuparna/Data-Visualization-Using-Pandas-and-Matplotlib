CREATE TABLE employment_ratios (
 'id' int(11) NOT NULL AUTO_INCREMENT,
 'country' text NOT NULL,
 'year' int(11) NOT NULL,
 'percentage_employment_to_population_ratio' decimal(10,2) NOT NULL,
 PRIMARY KEY ('id')
) 

CREATE TABLE employment_sector_measures (
 'id' int(11) NOT NULL AUTO_INCREMENT,
 'country' text NOT NULL,
 'gender' varchar(2) NOT NULL,
 'sector' varchar(3) NOT NULL,
 'year' int(11) NOT NULL,
 'percentage_sector_employment' decimal(10,2) NOT NULL,
 PRIMARY KEY ('id')
) 

CREATE TABLE working_population_measures (
 'id' int(11) NOT NULL AUTO_INCREMENT,
 'year' int(11) NOT NULL,
 'country' text NOT NULL,
 'gender' varchar(2) NOT NULL,
 'percentage_working_age_of_population' decimal(10,2) NOT NULL,
 PRIMARY KEY ('id')
) 