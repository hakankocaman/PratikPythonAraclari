# Practical Python Tools
This repostory contains practical tools encoded in Python. To use these tools, you need to have Python3 + installed on your computer. In addition, if the modules specified in the applications are not installed, you can install the related module by entering "pip install module" in the command line as stated in the description of the application.

## HavaTahmin.py (Weather Forecast Application)
This application provides real-time weather information using the OpenWeatherMap API. The application displays temperature, humidity, wind speed, atmospheric pressure, and sunrise/sunset times for any city in the world.

Project files are located under: `HavaTahmin/`

**Features:**
- 🌡️ Real-time temperature and "feels like" temperature
- 📅 5-day weather forecast
- ☁️ Weather condition descriptions in Turkish
- 💧 Humidity percentage
- 🌬️ Wind speed
- 📊 Atmospheric pressure
- 🌅 Sunrise and sunset times
- ❌ Comprehensive error handling

**Requirements:**
- Python 3.6+
- requests module (`pip install requests`)
- OpenWeatherMap API key (free at https://openweathermap.org/api)

**Usage:**
```bash
python3 HavaTahmin/HavaTahmin.py
```

**Future Enhancements (Daily Updates):**
- Day 3: Save favorite cities (JSON file)
- Day 4: Weather icons and emoji support
- Day 5: Compare multiple cities
- Day 6: Temperature graphs (matplotlib)
- Day 7: Weather alerts (extreme temperatures)

**🤖 Automated Daily Development:**
This project uses GitHub Actions to automatically add new features every day at 12:00 PM (Turkey time). The automation system:
- ✅ Adds one new feature per day following the roadmap above
- ✅ Automatically commits and pushes changes to GitHub
- ✅ Maintains consistent GitHub contribution activity
- ✅ Runs completely in the cloud (no local machine required)

**Development Progress:**
- Current Day: 3/7
- Next Feature: Favorite cities system
- Automation Status: Active ✅

You can manually trigger the workflow from the [Actions tab](https://github.com/hakankocaman/PratikPythonAraclari/actions) on GitHub.

**Folder Structure (HavaTahmin):**
- `HavaTahmin/HavaTahmin.py` → Main application
- `HavaTahmin/requirements.txt` → Dependencies for weather app
- `HavaTahmin/daily_update.py` → Daily auto-development script
- `HavaTahmin/development_plan.json` → 7-day feature plan state

## IP_Sorgulama.py
This application is coded to provide a quick list of IP addresses with the web services provided by https://ipstack.com/ . Requirements for the application to work;

- You must obtain an APIKEY by signing up at https://ipstack.com,
- You should assign the APIKEY you received from https://ipstack.com to the APIKEY variable in the code,
- If the requests module is not installed, you should install it by typing "pip install requests" on the command line.

For detailed content, see: https://www.hakankocaman.com/python-ile-pratik-araclar-ip-sorgulma

For the Medium article, see: https://medium.com/@hakankocaman/practical-tools-with-python-ip-query-541fa6df8cd9

Click on the picture below to access the Youtube video:
[<img src="http://www.hakankocaman.com/wp-content/uploads/PythonBanner.png" width="100%">](https://youtu.be/l2nR6o_rxfw)

## Coordinate Transformation

Using the Coordinate Converter tool, it is possible to convert the coordinate pairs in the “coordinate.txt” file in the same directory to their equivalent in another coordinate reference system using the services provided by EPSG.io. To do this, you need to do this by copying the coordinate pairs in the existing coordinate reference system with a space between them, saving the file and closing it. Then, after entering the EPSG codes of the existing and desired coordinate reference systems in the codes written in Python, in the relevant fields, run the code in your compiler. Thus, each of the coordinate pairs written in the coordinate.txt file will be converted into the coordinate reference system by the services provided by EPSG.io and printed into the “coordinate.txt” file and the process will be completed in this way.

For detailed content, see: https://www.hakankocaman.com/python-ile-pratik-araclar-koordinat-donusumu

For the Medium article, see: https://medium.com/@hakankocaman/practical-tools-with-python-coordinate-transformation-d8783efabda3

Click on the picture below to access the Youtube video:
[<img src="https://www.hakankocaman.com/wp-content/uploads/Coordinate_Transformation.png" width="100%">](https://youtu.be/PRK20-Wzeeo)

## MGRS Converter

You can access Python tool named MGRS Convertor and details, which allows you to quickly and quickly convert between the MGRS coordinate reference system and the WGS84 geographic coordinate reference system.

For detailed content, see: https://www.hakankocaman.com/python-ile-pratik-araclar-mgrs-donusturucu

For the Medium article, see: https://medium.com/@hakankocaman/practical-tools-with-python-mgrs-converter-fceac251780a

Click on the picture below to access the Youtube video:
[<img src="https://i2.wp.com/www.hakankocaman.com/wp-content/uploads/MGRS.png" width="100%">](https://youtu.be/DNg9HYekD0k)

## Google Elevation Api

Using Python and Google Elevation Api, WGS84 allows you to quickly and simply obtain the elevation value of geographic coordinates.

For detailed content, see: https://www.hakankocaman.com/python-ile-pratik-araclar-google-elevation-api

For the Medium article, see: https://medium.com/@hakankocaman/practical-tools-with-python-google-elevation-api-4e0231a94480

Click on the picture below to access the Youtube video:
[<img src="https://i2.wp.com/www.hakankocaman.com/wp-content/uploads/Google_Elevation_API.jpg?resize=800%2C400&ssl=1" width="100%">](https://youtu.be/S0OcNtyO3Fk)

## WEBb Site Alert

This application is coded by Hakan KOCAMAN for fast access control of websites. For more information and contact, you can visit www.hakankocaman.com and send an e-mail to İletişim@hakankocaman.com.

## Star History

## Star History

<a href="https://star-history.com/#hakankocaman/PratikPythonAraclari&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=hakankocaman/PratikPythonAraclari&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=hakankocaman/PratikPythonAraclari&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=hakankocaman/PratikPythonAraclari&type=Date" />
 </picture>
</a>
