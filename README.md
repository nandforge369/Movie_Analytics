Hi,

This project involves working with the datasets from The Movie Database (TMDB) and our goal is to load and preprocess the dataset, design and implement a well-structured relational SQL database, 
and execute a complete end-to-end data analytics pipeline encompassing SQL queries, Pandas-based EDA, data visualization, and the development of a comprehensive 
multi-page interactive dashboard using Streamlit. 

The datasets can be found already structured into a relational schema inside dataset folder in .csv format.

The work is divided in 4 different notebooks and one app.py file. 

Each of the four notebooks serve a unique purpose of the project as follows :

01_data_cleaning.ipynb involves Import the six provided CSV files, perform data cleaning by handling missing values and placeholders, eliminated duplicate records and orphaned entries, enforced appropriate data types, and load the cleaned datasets into the SQL database in separate tables by enforcing the same relation.

02_sql_analysis.ipynb involves establishing a connection to the SQL database (in our case MYSQL), import the cleaned tables, and finally solved all 10 SQL-based analytical questions.

03_pandas_analysis.ipynb involves Perform Pandas-based analysis to answer all 10 analytical questions, documenting each solution with a brief, meaningful insight.

04_visualizations.ipynb involves Univariate, bivariate, and multivariate visualizations using Matplotlib, Seaborn, and Plotly, with each visualization accompanied by a concise 2–4 sentence interpretation highlighting key findings and trends.

Appropriate markdowns are provided wherever necessary in each of the above four notebooks to aid in understanding of the logic and rationale.

<img width="1196" height="757" alt="image" src="https://github.com/user-attachments/assets/a2a7354c-78fc-41b2-8ee9-4ab5d2625b98" /></br>

The app.py file contains the multi-page Streamlit simulation which will allow the user to view and play with the data in a simpler way.

There are three tabs in app.py in the form of side bar - Filter, Dashboard and Query Explorer. 

The filter tab has certain specific widgets using which user can select the filter they like, and, in our backend, those are pushed to session state so that the filters are preserved for session. The filter section also displays number of movies which satisfies our current filter.

The dashboard tab provides a comprehensive summary and visualizations of the data as per the filter selected in filter tab along with a short summary.

Finally, the query explorer tab provides us the answer to the 10 SQL questions and supporting visulations or short summary.

The project folder is complete and has all the ingredients required to run the project. We just need to update the credentials for MY SQL DB.

Thanks!
