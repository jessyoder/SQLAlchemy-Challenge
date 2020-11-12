# SQLAlchemy-Challenge - Surfs Up!

I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, did some climate analysis on the area.

## Step 1 - Climate Analysis and Exploration

* I chose a start date and end date for my trip, December 23-31.

### Precipitation Analysis

* I designed a query to retrieve the last 12 months of precipitation data, collected the summary statistics, and plotted the results.

### Station Analysis

* I designed a query to find the most active stations based on which stations had the highest number of weather observations.

## Step 2 - Climate App

Once I completed my initial analysis, I designed a Flask API based on the data that I acquired. The app provides data including precipitation, stations, observed temperatures, and a function that allows a user to collect Max Temps, Avg Temps and Min Temps by entering in either a start date or a starting and ending date.
