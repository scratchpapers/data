## StubHub Major League Soccer (MLS) Games Scrape

### Using Selenium Webdriver, scraped StubHub website to get some info on Major League Soccer games

### One example is Los Angeles Galaxy

Website URL : https://www.stubhub.com/la-galaxy-tickets/performer/12587/

#### When scraping, the webpage detects and puts up a human verification check similar to CAPTCHA test

<img src='images/Human_Check.png'>

#### Once human verification check is completed, the Stub Hub website showing games are displayed

#### Sample view of Stub Hub page

<img src='images/Sample_Games_Site.png'>

#### When the scraper is run, the following result is shown. It scrapes info such as Home Team, Away Team, GameDate, GameName, Lowest Price ticket available, link to get the tickets, etc. This can be further expanded to get ticketing information

<img src='images/Sample_Games_Output.png'>


#### This mini project was done just for few MLS games, but the code can be expanded to get the ticket information for more teams. 4 of the teams are included in this example
