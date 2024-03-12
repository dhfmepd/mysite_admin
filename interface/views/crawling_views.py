import os
import urllib3
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
            os.environ['WDM_SSL_VERIFY'] = '0'

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            # Chrome 브라우저 열기
            # options = webdriver.ChromeOptions()
            options = Options()
            user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
            options.add_argument('user-agent=' + user_agent)
            options.add_argument('headless')

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

            # 페이지 연결시키기
            driver.get("https://finviz.com/quote.ashx?t=TSLA&p=d")

            # BeautifulSoup 객체 생성
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            print("Ticker :: " + soup.find('div', attrs={"class": "quote-header_ticker-wrapper"}).h1.text)
            print("Ticker Name :: " + soup.find('div', attrs={"class": "quote-header_ticker-wrapper"}).h2.text.strip())

            table = soup.find('table', {"class": "js-snapshot-table snapshot-table2 screener_snapshot-table-body"})
            trs = table.tbody.find_all('tr')

            mapData = dict()

            for index, tr in enumerate(trs):
                if index == 0:
                    print("P/E : " + tr.find_all('td')[3].text)
                    print("EPS : " + tr.find_all('td')[5].text)
                    mapData["per"] = tr.find_all('td')[3].text
                    mapData["eps"] = tr.find_all('td')[5].text
                if index == 1:
                    print("Forward P/E : " + tr.find_all('td')[3].text)
                    mapData["forward_per"] = tr.find_all('td')[3].text
                if index == 5:
                    print("ROE : " + tr.find_all('td')[7].text)
                    mapData["roe"] = tr.find_all('td')[7].text
                if index == 6:
                    print("Beta : " + tr.find_all('td')[11].text)
                    mapData["beta"] = tr.find_all('td')[11].text
                if index == 8:
                    print("RSI(14) : " + tr.find_all('td')[9].text)
                    mapData["rsi_14"] = tr.find_all('td')[9].text
                if index == 11:
                    print("Price : " + tr.find_all('td')[11].text)
                    mapData["price"] = tr.find_all('td')[11].text
                if index == 12:
                    print("Change : " + tr.find_all('td')[11].text)
                    mapData["change"] = tr.find_all('td')[11].text

            print(mapData)
            # 웹 페이지 종료
            driver.quit()

            resultDataForm = form.save(commit=False)
            resultDataForm.result_data = mapData
            resultDataForm.receipt_date = timezone.now()
            resultDataForm.save()
            return redirect('interface:crawling_main')
    else:
        form = ResultDataForm()
    context = {'form': form}
    return render(request, 'interface/crawling_main.html', context)
