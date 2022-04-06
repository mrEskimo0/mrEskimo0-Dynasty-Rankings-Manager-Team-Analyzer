# Dynasty Rankings Manager and League Analyzer Web Application

## 1. Description

This application serves as both a Dynasty Fantasy Football Rankings Manager and Dynasty Fantasy Football Team Analyzer. Creating and managing rankings is a task that most dynasty fantasy football players want to do, but using traditional tools such as Microsoft Excel or Google Sheets makes the task extremely painful and time-consuming. Speaking from experience, a task as simple as swapping rows of two players is a process of cutting and pasting a row 1 to the side, cutting and pasting row 2 in the desired position, and finally cutting and pasting row 1 from the side to it's desired position. That's a total of 3 cuts and pastes to simply swap 2 players. Maintaining rankings of 400+ players is an absolute nightmare. Rankings can then be mapped to a User's dynasty fantasy football league on Sleeper, the most popular Dynasty Fantasy Football platform. In the League Analyzer, users are presented with different graphs and charts to help visualize team values and make informed decisions in their leagues.

### Rankings Manager

The first feature of the application is a Rankings Manager. Using rankings templates, users can start making and adjusting their own dynasty fantasy football rankings without having to copy and paste a list of players and draft picks from the internet. The application offers ranking templates scraped from one of the most popular dynasty fantasy football sites, Keeptradecut.com, and actively managed rankings from 3rd and 20 Dynasty Podcast members. Users are given the following tools to help them make and adjust their own rankings with ease:
<ul>
  <li>Up & Down Arrows to Swap Players</li>
  <li>Number Box to Input Exact Player Values</li>
  <li>Adjustable Percentage Change Button</li>
  <li>Refresh Players Button to Insert New Players and Remove Retired Players</li>
</ul>

### League Analyzer

The second feature of the application is a Dynasty Fantasy Football League Analyzer. Using either user-created or featured ranking template sets, users can select a set of rankings to map to their League. Once a ranking set is mapped to their league, users will be presented with a page of charts and graphs on league-wide information:
<ul>
  <li>Total Value Bar Chart</li>
  <li>Total Player Value Bar Chart</li>
  <li>Positional Value Polar Area Charts</li>
</ul>

Users also have the ability to navigate to a team specific page. Team specific pages include a table of all the team's players and draft picks, with their ranking value, as well as team specific charts. The team specific charts are:
<ul>
  <li>Team Position Total vs League Median Radar Chart</li>
  <li>Total Team Value by Position Pie Chart</li>
</ul>

## 2. How It's Built

### Technologies

The backend of this application was built using Python Django + Django Rest Framework and a PostgreSQL database. I utilized the Python Pandas library to handle a lot of the data manipulation and mapping on the backend. The frontend was built using mainly vanilla Javascript, JQUERY, Bootstrap, HTML, and CSS. I used the Chart JS Javascript library for the charts in the League Analyzer. Docker and Docker-Compose were used to containerize the application, set up a Nginx reverse proxy, and deploy it on a linux server.

### Authentication
User creation follows the vanilla Django account creation system with some small overrides on the registration form to make the default name "John Dice" instead of "John Doe" (a much needed change). The application authenticates users via session authentication, except for two api calls which are explained in the section below.

### Rankings Manager
On the rankings side of the application I built two Rest APIs with token authentication that are called to update the rankings sets that are scraped from Keep Trade Cut and Update any changes in the Sleeper player database. Player rankings are "Ranking" objects in the database, which are children of Player objects. Rankings then all point to a single "User Ranking" instance, a child of Ranking in the database. Structuring the database this way made it so player objects are never directly being changed, and by grouping all the "Rankings" into a single "User Ranking", it made mapping rankings objects to players in the league analyzer and dashboard much cleaner. When a player's value is changed the frontend sends an AJAX post request to the server with only objects that have had their value's altered, the ranking is first saved to a ranking history table before getting saved to the database. For the default rankings, any users that aren't administrators are returned a html page without the submit and refresh players button, to prevent unwanted changes to templates. The "Refresh Players" button compares the players (and draft picks) in the consensus rankings to the current rankings, and deletes players that don't exist in the Consensus but do exist in the current, and adds players that exist in the consensus that don't in the current.  I used the Django Filters library for the ranking filters, with some Javascript to ensure all the position boxes are checked when filtering by all positions.

Creating and Updating rankings use the same form, but when updating the form is pre-filled using the ranking selected. These forms we're built using Django's ModelForms, but I added an extra field for the choose rankings passing a custom queryset with the template rankings.

### League Analyzer
Initially the application was supposed to just be a rankings manager, but as a developer I had to find a way to make the application more complicated than it needed to be. </jk> This came in the form of a league analyzer. When a user views their league, I hit the Sleeper API to get the teams and players in the league. Players are first mapped to the display name of the team they belong to, and secondly are mapped to their corresponding value in the user selected ranking set. For any players that don't exist in the ranking set, I set their value to 0. The draft picks of each team aren't given a roster ID like the players in the Sleeper API response, only the trades of the picks are returned. I had to write a function to create the draft picks and map them to the correct teams via the trades response.

Once everything is mapped, I save this information in the form of a Pandas dataframe to the database. Pandas has a df.to_sql command that I was able to take advantage of to avoid looping through the dataframe and saving each row one at a time. I created REST API responses for each of the charts on the front end from the dataframe saved in the database, and I pass through the names of all the teams in a context dictionary. Each team in the league can be selected and viewed in detail in a new page. I also created API endpoints for the team specific charts and table. All of the charts we're created using Chart JS and colored using a color algorithm to adjust the alpha value based on the how many standard deviations above or below the average the chart values are. Chart JS plugins we're also used to serve the team names on the slices of the polar area charts on the league page.

### Deployment
The application was deployed using Docker and Docker-Compose on a Linux server on Digital Ocean. Static files are served directly from the server via a Nginx reverse proxy and all other requests are routed to the Django project to be routed. The project code on Github is connected to the server, so any updates can be tested on my local development server, and pushed to Github and pulled into production with ease. I set up logging on the server to get information on errors level 500 and above while the application is live.
