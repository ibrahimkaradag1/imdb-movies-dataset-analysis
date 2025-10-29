# IMDb Movies Dataset Analysis

This project demonstrates a complete data pipeline using Python, SQLite, and Power BI.  
The goal is to clean, process, and visualize IMDb movie and TV show data.


## Project Structure

Imdb Project/

┣ data/ ← Raw dataset (IMDB.csv)

┣ src/ ← Python scripts for data processing

┣ exports/ ← Cleaned datasets ready for visualization

┣ imdb.sqlite ← SQLite database file

┣ IMDb_Dashboard.pbix← Power BI dashboard

┣ .venv/ ← Virtual environment (ignored in Git)

┗ README.md


## Workflow Overview

| Step | Description | Tool |
|------|--------------|------|
| 1 | Create virtual environment and install dependencies (pandas, sqlite3) | Python |
| 2 | Load the IMDb dataset (CSV) | pandas |
| 3 | Clean and transform the data (normalize columns, fix types, remove invalid rows) | Python |
| 4 | Store the cleaned data in a SQLite database | SQLite |
| 5 | Export the processed data to CSV | pandas |
| 6 | Create an analytical dashboard | Power BI |


## Key Features

- Data cleaning and normalization  
- Automatic classification of movies and TV shows  
- Filtering of invalid or missing records  
- Storage of both raw and cleaned tables in SQLite  
- Export of final dataset for Power BI visualization  


## Technologies Used

- Python 3.12+  
  - pandas  
  - sqlite3  
  - pathlib  
- SQLite  
- Power BI Desktop  
- Git and GitHub  
