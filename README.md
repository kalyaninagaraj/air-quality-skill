# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/smog.svg" card_color="#6C7A89" width="50" height="50" style="vertical-align:bottom"/> Air Quality
Mycroft reports real-time pollutant levels in your city.

## About
Get real-time air quality data for more than 1000 cities from 
the [World Air Quality Index](https://aqicn.org/) (WAQI) project. 

By default, Mycroft reports **real-time** (most recent, 
one-hour average) fine particulate matter (PM 2.5) concentration 
levels at a monitoring station in your city. You can also ask 
Mycroft for PM 10, carbon monoxode (CO), nitrogen dioxide 
(NO<sub>2</sub>), and sulphur dioxide (SO<sub>2</sub>) levels at 
your location or in other cities. Mycroft will also report how 
long back the reading was taken if the measurements were made more 
than two hours ago, and a health cautionary statement (only for 
PM 2.5 concentration levels) as suggested by the WAQI project. 

The Air Quality skill requires an API key to access data from 
the World Air Quality Index project. For instructions to obtain 
a key, go to the skill settings in your Mycroft account. The 
WAQI project's terms of acceptable data and API usage apply.  

### Things to note
* Several stations record ozone levels but the WAQI project's 
API doesn't mention the units (ppb, or milligrams per cubic meter).
So, for the present, this skill doesn't report ozone levels.
* Different government agencies have different air quality standards, 
resulting in different nations using different air quality indices. To 
standardize the reporting, this skill reports *raw* concentration 
levels measured in micrograms per cubic meter.  

## Examples
* "What is the air quality?"
* "How polluted is the air in New Delhi?"
* "What is the carbon monoxide level in Hong Kong?"
* "What's the ozone level in Dublin?"
* "What's the PM 10 level in Portland?"

## Credits
[@kalyaninagaraj](https://github.com/kalyaninagaraj)

## Category
**Daily**
Information

## Tags
#Air quality
#Pollutant level
#Mycroft AI
