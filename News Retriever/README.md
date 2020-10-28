# Web Scraping "El Tiempo"

In this part of the project I develop a code able to web scrape the main page of El tiempo. Searching and saving the articles that could be access through main page of the website. During the duration of this project, the [El Tiempo Webpage](https://www.eltiempo.com/) remain unchanged in its structure, therefore the structure of the web scraping code never suffer any fundamental changes. Also the extraction period went from April 13 to August 3. The articles were extracted in a daily basis, at 8pm Colombian hour. The process was automated by creating a bat file and a daily task for the computer to run. Nevertheless, it is important to state that for logistical reasons my computer was not switched on some of these days, and causing that some days the webpage was not scraped. These days are: May 08,12,15,18-19,23-24,May 27 to June 1, June 4-14,19,21,25,July 03,11,14-1

## Data Collected.

At the end, the program was able to collect the news from around 80 different days, giving us around 2000 articles. Allowing us to correctly retrieved and structured the data for its later processing, before inputting the data in the LDA model. 

If you are interested in the code I created to web scrape just check the ".py" file and/or if you are interested in using the news files they are available in the "El_Tiempo" directory. 
