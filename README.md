# Events Crawler
As requested by the company, this project was built to set up a crawler to store data in a 
self defined Postgres database to show a plot with the events count per date.

## Features
- Event crawler
- Postgres database built with `docker-compose`
- Data insertion into the database
- Plotting the data based on the events amount per day


## Getting Started

### Requirements
- Python 3.8 or higher
- Pipenv (optional, but recommended for managing dependencies)

### 1. Installing Required Dependencies
- [Clone the repository](https://github.com/jorgesisco/summer-festival-crawler)
- Navigate to the project folder
    ```
    cd summer-festivals-crawler
    ```
- (Optional) If you're using Pipenv, create a virtual environment and install dependencies.

  ```
  make install
   ```
    it will install pipenv with the dependencies from the requirement.txt

**Be sure the python virtual environment is set for this project.**

### 2. Database Credentials Setup

For this challenge, the database credentials were hardcoded for demonstration purposes and since this is a 
small-scale prototype it was the proper option.

### 3. Running the application

- Be sure your Docker dameon is up and running.
- To run the application, execute the following command from the project's root:

```
make build
```

This command is executing `docker-compose build` and `docker-compose up`, then after finishing building
it will run the main.py file and proceed with the database creation (first run), crawling the data, and 
running the plotter method.

If you want to stop and remove all containers, networks, and volumes created by `make build` command type:

```commandline
make down
```

**Note:** Check the method's parameter `active` to be set to ```True``` in order to run adding the crawled data in the database.

## View the Tables
Any database viewer can help you take a look at the database and the diagram, in the other hand I took the time to set up adminer and it can be accessed by goint to:
```commandline
http://localhost:8080/
```

## Approach for the Project

### 1. Built the crawler using beautiful soup
  - Crawler `class` includes the bs4 initialization, along with a `get_links` method to extract all event links and  `find_elements` 
    method that based on the given parameters it will look for the html defined tag to extract the desired text or array of text.
  - In the crawler file I also made two helper functions to help me extract urls.
  - `get_event_data` method calls `find_elements` for each data we want to extract and returns it in a `dict()`.


### 2. Established an [ERD](https://lucid.app/lucidchart/49b71880-5d38-4417-bc30-c71fa126a02a/edit?viewport_loc=-245%2C-41%2C2699%2C1543%2C0_0&invitationId=inv_d12a4f2f-7d5d-42b8-873a-18e178b3b60c)
Based on the extracted data, I got a better idea on how to establish the database tables distribution and relationships.

#### ERD description:

  - **locations table:**
    - `One-to-many` relationship with `events` table (one location can have many events)
    - **Type:** Parent


  - **events table:**
    - `Many-to-one` relationship with `locations` table (Multiple events can have the same location)
    - `One-to-many` relationship with `works` (one event can have many works)
    - `One-to-many` relationship with `event_artists` table (one event can have many artists)
    - `One-to-many` relationship with `event_dates` table (one event can have many dates)
    - `One-to-many` relationship with `event_tickets` table (one event can have many tickets)
    - **Type:** Child and Parent
  

- **works table:**
    - `Many-to-one` relationship with `events` table (one work can belong to many events)
    - **Type:** Child


- **artists table:**
    - `Many-to-many` relationship with `events` table through `event_artists` table (one artist can perform in many events, one event can have many artists)
    - **Type:** Child


- **event_artists table:**
    
  - `Many-to-many` relationship with `artists` table and `events` table
  - **Type:** Association
  

- **dates table:**
    
    - `Many-to-many` relationship with `events` table through `event_dates` table (one date can have many events, one event can occur on many dates)
    - **Type:** Child
  

- **event_dates table:**
    
    - `Many-to-many` relationship with `events` table and `dates` table
    - **Type:** Association
  

- **tickets table:**
    
    - `Many-to-many` relationship with `events` table through `event_tickets` table (one ticket can belong to many events, one event can have many tickets)
    - **Type:** Child
 
 
- **event_tickets table:**
  - `Many-to-many` relationship with `events` table and `tickets` table
  - **Type:** Association

## 3. Database
- Built a class with methods to create the tables by using `psycopg2`, and adding data to each table based on the crawled data.

## 4. Plotting the Data
- Built a function which uses `psycopg2` to query the `tables`, `event_dates` and `events`, to make a view with the dates and event count, then I used matplotlib to plot the data.
- 

[Plotted Data Screenshot](https://drive.google.com/file/d/1_8RyCyTgTkJtaEoNztvaw2qSf-MT5xY0/view?usp=share_link)

##  Considerations
 - The challenge was based on the provided scope by the recruiter, building crawler, database (docker-compose), insert data and plot the
   data based on the specified query.
 - It was not clear enough what `works` is supposed to be, I assumed it was referring to the Programs info I saw on each 
event.
 - One thing that needs improvement is the crawler to make it extract the data in a more refined way, if the website
is updated and something changes, then some data structures like `dictionaries` will require updates.
 - I would have used Octoparse for extracting the data, it will always depend on the scope and analyzing if it is a good approach.