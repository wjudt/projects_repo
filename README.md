## Hello everyone!
My name is Wojciech Judt. I try to explore the secrets of data exploration. I am interested in application of data engineering tools in real life. I want to show you what i have done so far :).

### First project - cleaning computer jobs offers 
Main used libraries and tools: python 3.8, pandas 1.4.3, matplotlib 3.3.4

My first project is connected with clearing a raw dataset, which I found at kaggle.com. Mentioned dataset contains 622 computer job offers scraped from glassdoor.com. I read raw data from csv file, then cleaned them. I prepared this dataset also for doing some simple data science on it. After that I showed some crucial information about the dataset on a few charts. After that cleaned dataset was written to a new csv file for further use.

Project location: 
- ./computer_jobs_cleaning_and_analysis
Code: 
- All code in a file: Cleaning_computer_jobs_dataset.ipynb
Data: 
- raw data in a file: uncleaned_computer_jobs_original.csv
- cleaned data in a file: cleaned_computer_jobs.csv
      
### Second project - preparing SQL dimensional database model based on a scraped data
Main used libraries and tools: python 3.8, pandas 1.4.3, numpy 1.20.1, beautifulsoup4 4.9.3, pysftp 0.2.9, pyodbc 1.3.5, Micrsoft SQL Server 2019, Microsoft SQL Server                                  Managment Studio 18

My second project is a first bigger project. In the first part of the project I used beautifulsoup library to scrap data from beeradvocate.com webpage. Scraped data due to problems with connection to a webpage were scraped into eight separated json files. All files were collected into one directory and were concatenated into one DataFrame. It was 180 thousand of records. After that I cleaned scraped data and I wrote them into hdf file. Then I made a connection with a previously created sftp server and add this file into it. 
Second part of the project was connected with preparation of a dimensional model for a data warehouse. I downloaded the earlier hosted hdf file from sftp server and I read him as a DataFrame. Then I prepared a dimensional model of data warehouse, which was a simple snowflake schema. Database was located at Micrsoft SQL Server 2019, which whom i connected via pyodbc library. Database model was composed of eight tables, which one was fact table and seven was dimension tables. All tables, keys and data was created/added into a database via SQL code. SQL Server Managment Studio was used only for the evaluation of the correctness of the performed operation and schema/tables visualisation, which was added into Jupyter notebook for easier understanding.
Third part is connected with developing several queries of varying complexity for the created database model and will be prepared in a few days.

Project location: 
- ./beer_ranking_web_scraping
Code: 
- First part: Web_scraping.ipynb
- Second part: SQL_database_preparation.ipynb
- Third part: SQL_select_queries.ipynb

Data: 
- scraped data in a folder: ./beer_ranking_web_scraping/json_files
- cleaned DataFrames saved as hdf files in a folder: ./beer_ranking_web_scraping/hdf_files
- sftp server is located in a folder: ./database_for_projects/sftp_server
- data downloaded from a sftp server in a folder: ./beer_ranking_web_scraping/downloaded_from_sftp

### Third project - to be continued :)
