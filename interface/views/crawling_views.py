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

def exch_data_call(mapData, soup):
    mapData["Exch Rate"] = soup.find('div', attrs={"data-test": "instrument-price-last"}).text

def market_data_call(mapData, soup):
    lis = soup.find('div', attrs={"id": "market-summary"}).find_all('li')
    for index, li in enumerate(lis):
        keyword = li.find('a')['title'].strip()
        mapData[keyword] = li.find('fin-streamer').text.strip()