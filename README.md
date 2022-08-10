## Hello everyone!
My name is Wojciech Judt. I try to explore the secrets of data exploration. I am interested in application of data engineering tools in real life. I want to show you what i have done so far :).

### First project - cleaning computer jobs offers 
Main used libraries and tools: python 3.8, pandas 1.4.3, matplotlib 3.3.4

My first project is connected with clearing a raw dataset, which I found at kaggle.com. Mentioned dataset contains 622 computer job offers scraped from glassdoor.com. I read raw data from csv file, then cleaned them. I prepared this dataset also for doing some simple data science on it. After that I showed some crucial information about the dataset on a few charts. After that cleaned dataset was written to a new csv file for further use.

Project location: 
- ./computer_jobs_cleaning_and_analysis

Code and data location: 
- All code is present in a file: ./computer_jobs_cleaning_and_analysis/Cleaning_computer_jobs_dataset.ipynb
- Raw data is located in a file: ./computer_jobs_cleaning_and_analysis/uncleaned_computer_jobs_original.csv
- Cleaned data is located in a file: ./computer_jobs_cleaning_and_analysis/cleaned_computer_jobs.csv
      
### Second project - preparing SQL dimensional database model based on a scraped data
Main used libraries and tools: python 3.8, pandas 1.4.3, numpy 1.20.1, beautifulsoup4 4.9.3, pysftp 0.2.9, pyodbc 1.3.5, Micrsoft SQL Server 2019, Microsoft SQL Server                                  Managment Studio 18, Power BI Desktop

My second project is a first bigger project. In the first part of the project I used beautifulsoup library to scrap data from beeradvocate.com webpage. Scraped data due to problems with connection to a webpage were scraped into eight separated json files. All files were collected into one directory and were concatenated into one DataFrame. It was 180 thousand of records. After that I cleaned scraped data and I wrote them into hdf file. Then I made a connection with a previously created sftp server and add this file into it.  
  
Second part of the project was connected with preparation of a dimensional model for a data warehouse. I downloaded the earlier hosted hdf file from sftp server and I read him as a DataFrame. Then I prepared a dimensional model of data warehouse, which was a simple snowflake schema. Database was located at Micrsoft SQL Server 2019, which whom I connected via pyodbc library. Database model was composed of eight tables, which one was fact table and seven was dimension tables. All tables, keys and data was created/added into a database via SQL code. SQL Server Managment Studio was used only for the evaluation of the correctness of the performed operation and schema/tables visualisation, which was added into Jupyter notebook for easier understanding.  
  
Third part is connected with developing a few sql queries of varying complexity on a created database, which their task is finding answers to the six posed questions. Queries were composed in Microsoft SQL Server Managment Studio 19. Posed questions for making dashbords:
- How the rolling total of beers launched each year and the average rating for the three breweries that achieved the highest rating and had more than 100 beers in their range looks over time.
- What are the most popular styles of beers from the US and Russia. How much alcohol they had.
- What the beer market looks like in the Michigan and Georgia states.
- Which beer is most wanted in US, which style have most rating in different countries, which beer has best rating for each US states.
- How many beers from US was added to the scraped webpage in years 2018-2022 in each month.
- Whether the number of beers which was added to the scraped webpage depends on the month of the year.  
  
During the fourth part of the project I prepared a few business dashboards in Power BI Desktop, both static (when you cannot have interaction with a dashboard) and dynamic (opposite to static), according to posed questions, which are located above. I read data from prepared earlier SQL Server database (both using queries and views). Dashboards were also exported into pdf file, if you do not have installed Power BI Desktop but you can not use dynamic features using pdf versions.
  
Project location: 
- ./beer_ranking_web_scraping/

Code and data location: 
- **First part:** ./beer_ranking_web_scraping/Web_scraping.ipynb  
Scraped data are located in the folder: ./beer_ranking_web_scraping/json_files/  
Cleaned DataFrames saved as hdf files are located in the folder: ./beer_ranking_web_scraping/hdf_files/  
Sftp server is located in the folder: ./database_for_projects/sftp_server/  
Data downloaded from a sftp server are located in the folder: ./beer_ranking_web_scraping/downloaded_from_sftp/
- **Second part:** ./beer_ranking_web_scraping/SQL_database_preparation.ipynb
- **Third part:** ./beer_ranking_web_scraping/sql_queries/
- **Fourth part:** ./beer_ranking_web_scraping/power_bi_dashboards/

### Third project - to be continued :)
