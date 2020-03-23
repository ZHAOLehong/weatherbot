import json
import requests

def getCityCode(city_name):

    cityInfo = json.load(open("/Users/zachary/Desktop/weatherbot/util/weather_api/city.json"))
    for city in cityInfo:
        if (city["city_name"] in city_name or city_name in city["city_name"]) and city["city_name"] != "吉林":
            return city["city_code"]

def getWeatherInfo(city_name, date=0):
    """date = 0 默认当天 data<=14"""
    city_code = getCityCode(city_name)
    content = requests.get("http://t.weather.sojson.com/api/weather/city/{}".format(city_code)).text
    city_info = json.loads(content)
    weather = city_info["data"]["forecast"][date]
    shidu = city_info["data"]["shidu"]
    return weather, shidu

if __name__ == '__main__':
    print(getWeatherInfo(city_name="北京"))

