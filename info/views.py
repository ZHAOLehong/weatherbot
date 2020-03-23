from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from util.weather_api.utils import getWeatherInfo
import requests
import json
import time
import datetime
# Create your views here.

class WebhookView(View):

    def get(self, request):
        retJosn = {
            'Msg': "Test OK",
        }
        return JsonResponse(data=retJosn, safe=False)

    def post(self, request):

        req = json.loads(request.body)
        print(req)
        # get action from json
        date2 = req.get('queryResult').get('parameters').get('datetime')[:10] #date2: '2020-3-20'
        if type(date2) == type([]) and date2 != []:
            # 处理昨天这种情况
            date2 = date2[0][:10]
        location = req.get('queryResult').get('parameters').get('location').get('city')
        if location=='':
            location = req.get('queryResult').get('parameters').get('location').get('country') #香港 台湾 澳门

        choice = req.get('queryResult').get('parameters').get('weather')
        date1 = time.strftime('%Y-%m-%d', time.localtime(time.time())).split('-')
        if date2 == '' or date2== []:
            date2 = date1
        else:
            date2 = time.strptime(date2, "%Y-%m-%d")
        date1 = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]))
        date2 = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]))
        day = date2 - date1
        if day.days >= 0 and day.days <= 14:
            weather, shidu = getWeatherInfo(city_name=location, date=day.days)
        else:
            fulfillmentText = {'fulfillmentText': '小天暂时查询不到您说的天气呢～小天只能查询今天和未来14天内天气哦～'}
            return JsonResponse(fulfillmentText, safe=False)
        date2 = str(date2)[:10]

        if choice == "湿度":
            fulfillmentText = {'fulfillmentText': '{}{}的湿度是{}～'.format(location,date2,shidu)}
        elif choice == "最高气温":
            fulfillmentText = {'fulfillmentText': '{}{}{}～'.format(location,date2,weather['high'])}
        elif choice == "最低气温":
            fulfillmentText = {'fulfillmentText': '{}{}{}～'.format(location,date2,weather['low'])}
        elif choice == "风力":
            fulfillmentText = {'fulfillmentText': '{}{}{}{}～'.format(location, date2, weather['fx'],weather['fl'])}
        else:
            fulfillmentText = {'fulfillmentText': '{},{},{},{},{},湿度{},{},{},{}～'.format(location,date2,weather['type'], weather['high'],
                                                                                    weather['low'], shidu,weather['fx'],weather['fl'],weather['notice'])}
        return JsonResponse(fulfillmentText, safe=False)
