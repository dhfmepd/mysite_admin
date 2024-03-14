import os
import sys
import urllib3
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ..forms import ResultDataForm

@login_required(login_url='common:login')
def main(request):
    if request.method == 'POST':
        form = ResultDataForm(request.POST)
        if form.is_valid():
            resultDataForm = form.save(commit=False)

            user_agent = resultDataForm.user_agent
            target_url = resultDataForm.target_url

            os.environ['WDM_SSL_VERIFY'] = '0'

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            # Chrome 브라우저 열기
            if not user_agent:
                options = webdriver.ChromeOptions()
            else:
                options = Options()
                options.add_argument('user-agent=' + user_agent)
            options.add_argument('headless')

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

            # 페이지 연결시키기
            driver.get(target_url)

            # BeautifulSoup 객체 생성
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            base_data = resultDataForm.base_data
            base_data = base_data.replace("'", "\"")

            if not base_data:
                mapData = dict()
            else:
                mapData = json.loads(base_data)

            getattr(sys.modules[__name__], resultDataForm.func_name)(mapData, soup)

            # 웹 페이지 종료
            driver.quit()

            resultDataForm.result_data = json.dumps(mapData)
            resultDataForm.receipt_date = timezone.now()
            resultDataForm.save()

            return render(request, 'interface/crawling_result.html', {'result': resultDataForm})
    else:
        form = ResultDataForm()
    context = {'form': form}
    return render(request, 'interface/crawling_main.html', context)

def finviz_data_call(mapData, soup):
    mapData["Ticker"] = soup.find('div', attrs={"class": "quote-header_ticker-wrapper"}).h1.text
    mapData["Ticker Name"] = soup.find('div', attrs={"class": "quote-header_ticker-wrapper"}).h2.text.strip()

    table = soup.find('table', {"class": "js-snapshot-table snapshot-table2 screener_snapshot-table-body"})
    trs = table.tbody.find_all('tr')

    for trIdx, tr in enumerate(trs):
        tds = tr.find_all('td')
        for tdIdx, td in enumerate(tds):
            if tdIdx % 2 == 0:
                keyword = td.text.strip()
                mapData[keyword] = tds[tdIdx + 1].text.strip()

    table = soup.find('table', {"class": "js-table-ratings styled-table-new is-rounded is-small"})
    trs = table.tbody.find_all('tr')

    rating_list = list()

    for trIdx, tr in enumerate(trs):
        tds = tr.find_all('td')
        rating_dict = dict()
        rating_dict['Date'] = tds[0].text
        rating_dict['Action'] = tds[1].text
        rating_dict['Analyst'] = tds[2].text
        rating_dict['Rating Change'] = tds[3].text
        rating_dict['Price Target Change'] = tds[4].text
        rating_list.append(rating_dict)

    mapData['Rating List'] = rating_list

def exch_data_call(mapData, soup):
    div = soup.find('div', attrs={"data-test": "instrument-header-details"})
    mapData["Exch Rate"] = div.find('div', attrs={"data-test": "instrument-price-last"}).text
    mapData["Exch Rate Change"] = div.find('span', attrs={"data-test": "instrument-price-change"}).text
    mapData["Exch Rate Change Percent"] = div.find('span', attrs={"data-test": "instrument-price-change-percent"}).text.replace('(', '').replace(')', '')

def index_data_call(mapData, soup):
    trs = soup.find('div', attrs={"data-yaft-module": "tdv2-applet-smpl-data-tbl"}).find_all('tr')
    for index, tr in enumerate(trs):
        if index > 0:
            keyword = tr.find('td', attrs={"aria-label": "Name"}).text.strip()
            mapData[keyword] = tr.find('td', attrs={"aria-label": "Last Price"}).text.strip()
            keyword = keyword + ' Change'
            mapData[keyword] = tr.find('td', attrs={"aria-label": "Change"}).text.strip()
            keyword = keyword + ' Percent'
            mapData[keyword] = tr.find('td', attrs={"aria-label": "% Change"}).text.strip()

def crypto_data_call(mapData, soup):
    trs = soup.find('div', attrs={"data-yaft-module": "tdv2-applet-smpl-data-tbl"}).find_all('tr')
    for index, tr in enumerate(trs):
        if index > 0:
            keyword = tr.find('td', attrs={"aria-label": "Name"}).text.strip()
            mapData[keyword] = tr.find('td', attrs={"aria-label": "Price (Intraday)"}).text.strip()
            keyword = keyword + ' Change'
            mapData[keyword] = tr.find('td', attrs={"aria-label": "Change"}).text.strip()
            keyword = keyword + ' Percent'
            mapData[keyword] = tr.find('td', attrs={"aria-label": "% Change"}).text.strip()

def tech_data_call(mapData, soup):
    section = soup.find('section', attrs={"data-test": "cwl-symbols"})
    trs = section.find_all('tr')
    result_list = list()
    for index, tr in enumerate(trs):
        if index > 0:
            result_data = dict()
            result_data['no'] = index
            result_data['symbol'] = tr.find_all('td')[0].text.strip()
            result_data['name'] = tr.find_all('td')[1].text.strip()
            result_data['price'] = tr.find_all('td')[2].text.strip()
            result_data['change'] = tr.find_all('td')[3].text.strip()
            result_data['change_percent'] = tr.find_all('td')[4].text.strip()
            result_list.append(result_data)

    mapData['tech_list'] = result_list
