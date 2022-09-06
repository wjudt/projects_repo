## Hello everyone!
My name is Wojciech Judt. I try to explore the secrets of data. I am interested in application of data engineering tools in real life. I want to show you what i have done so far :).

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

### Third project - preparing a dataflow, which is used during an analysis of air traffic above a choosen part of polish sky
Main used libraries and tools: python, pandas, pytest, apache-airflow, docker, minio (AWS S3 opensource equivalent), postgres, OpenSkyAPI,  Microsoft Power BI - details in requirements.txt file

Third project was relied on collecting data from the OpenSkyAPI (https://openskynetwork.github.io/opensky-api/python.html), from the area showed on a figure 1 (all figures which will be mentioned in that part are located in ./docs/figures/). Analysed area has about 30.5 thousands square kilometres (figure 2).  
Everything is orchestrated together in Apache-Airflow environment. Graph and task grid obtained in Airflow for composed DAG is showed in figures 4 and 5. The Airflow is installed inside a docker container. The data is read from API once per 15 minutes and saved in a raw bucket at a Minio server in .csv file(figure 3). Then data is cleaned and saved in a clean bucket at the same Minio server in .csv file.  
Data cleaning is realized by a python script, for which I have prepared a few unit tests according to the TDD methodology. After that data is downloaded from clean bucket and added into Postgres database, which is configured inside a docker container. Containers were configured in docker-compose.yaml files.  
Database preview and SQL code preparation, which is necessary for making a table, removing duplicated data and copy data from .csv file is realized in the DBeaver tool (figure 6). Whole project is prepared in the virtual environment with using of the PyCharm tool. Data collected inside the Postgres database are grouped via sql script (preparation of a view), which is used for making a dynamic dashboard in Power BI software. Mentionad dashboard sumarize 
Version 0.1 of the project has some problems with access permissions after sending cleaned data into Postgres database container. It requires manual entering into a Postgres container and set permissions for new files – new files do not inherit permissions defined for a directory. Then everything works as it should. I have to repair that feature in the next version of the project. 
  
Project location: 
- ./air_traffic_with_airflow/

Code and data location: 
- **DAG:** ./air_traffic_with_airflow/dags/opensky_api_v9.py  
- **data cleaning module:** ./air_traffic_with_airflow/dags/packages/modules.py  
- **SQL queries:** ./air_traffic_with_airflow/dags/sql_queries/
- **Minio server:** ./air_traffic_with_airflow/minio
- **Unit tests:** ./air_traffic_with_airflow/tests/test_modules.py
- **Example of raw and clean data file:** ./air_traffic_with_airflow/docs/
- **Dashboard:** ./air_traffic_with_airflow/power_bi_dashboard/

### Project number 3.5 - making an API
Main used libraries and tools: python, fastapi, SQLAlchemy, pydantic, uvicorn, postman  - details in requirements.txt file
  
The API allows reading data from a database, which was prepared in the third project. So from CRUD utilities this API realize only read function. We have three posibilities to read data from a database by the API: 
- First request allows for obtaining all flights, but it use a skip and limit parameters for presented records. 
- Second request allows for obtaining a single flight by icao24 code. 
- Third request choose records from a database in a defined period of time according to a date of DAG execution.  
Example request results from a postman app and a shortcut from the fastapi automatic documentation are presented in the 'screenshots' folder.
  
Project location: 
- ./api_to_postgres_db/
