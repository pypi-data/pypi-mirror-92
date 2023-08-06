# Weather-Forecast

A Python script that displays the 5-day weather forecast (3 hour intervals) for a given location. This was implemented using the pyOWM API (Open Weather Map). 

Locations can be searched by city name, postal code, or coordinates. Furthermore, after searching a given location, the forecast is printed to the console. After the forecast finishes, the user is prompted to search for another location. The script doesn't terminate until the user exits. Just before terminating, the forecasts for any search locations are dumped to a .csv file.

## Requirements
#### Python
You need Python 3.4 or later to run this script. You can have multiple Python versions (2.x and 3.x) installed on the same system without issue.

In Ubuntu, Mint and Debian you can install Python 3 like this:
```
$ sudo apt-get install python3 python3-pip
```
For other Linux flavors, macOS and Windows, packages are available at <https://www.python.org/getit/>

#### Pyowm
Furthermore, you need the PyOWM wrapper library for OpenWeatherMap web APIs installed locally. The dependency can be installed through the pip installer like this:
```
$ pip install pyowm
```
