# Practical Python Tools
This repostory contains practical tools encoded in Python. To use these tools, you need to have Python3 + installed on your computer. In addition, if the modules specified in the applications are not installed, you can install the related module by entering "pip install module" in the command line as stated in the description of the application.

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
