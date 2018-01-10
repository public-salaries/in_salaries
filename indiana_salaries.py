import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

#--------------------define variables-------------------
# START_YEAR = '2016'
# START_COUNTY = 'Marion'
#-------------------------------------------------------

class IndianaScraper:
    def __init__(self,
                 base_url='https://gateway.ifionline.org/report_builder/Default3a.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetYearAndCountyList(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Length': 7466,
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'ASP.NET_SessionId=wvzwjr55vc4v2555s45l4f45; __utma=6658980.107443296.1515250060.1515250060.1515250060.1; __utmc=6658980; __utmz=6658980.1515250060.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=6658980.1.10.1515250060',
            'Host': 'gateway.ifionline.org',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        self.session.headers = headers

        # set post data
        params = {}
        params['rpttype'] = 'employComp'
        params['rpt'] = 'EmployComp'
        params['rptName'] = 'Employee Compensation'

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, params=params)
        self.session.cookies.set('ASP.NET_SessionId', ret.cookies.get('ASP.NET_SessionId'))

        if ret.status_code == 200:
            # get year list
            years = []
            options = Selector(text=ret.text).xpath('//select[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option').extract()
            for idx in range(1, len(options)):
                years.append({
                    'text': Selector(text=options[idx]).xpath('//option/text()').extract()[0],
                    'value': Selector(text=options[idx]).xpath('//option/@value').extract()[0]
                })
            print(years)

            # get county list
            counties = []
            options =Selector(text=ret.text).xpath('//select[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option').extract()
            for idx in range(1, len(options)):
                counties.append({
                    'text': str(Selector(text=options[idx]).xpath('//option/text()').extract()[0]).replace('\xa0', ' '),
                    'value': Selector(text=options[idx]).xpath('//option/@value').extract()[0]
                })
            print(counties)

            # get unit list
            unit_list = []
            options = Selector(text=ret.text).xpath('//select[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option').extract()
            for idx in range(1, len(options)):
                unit_list.append({
                    'text': str(Selector(text=options[idx]).xpath('//option/text()').extract()[0]).replace('\xa0', ' '),
                    'value': Selector(text=options[idx]).xpath('//option/@value').extract()[0]
                })
            print(unit_list)

            # get form data
            self.form_data = {}
            # get ControlID
            scripts = Selector(text=ret.text).xpath('//script').extract()
            for script in scripts:
                if 'ControlID=' in script:
                    self.form_data['ControlID'] = str(script).split('ControlID=')[1].split('"')[0]

            self.form_data['__VIEWSTATE'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0]
            self.form_data['__VIEWSTATEGENERATOR'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            self.form_data['__EVENTVALIDATION'] = Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]

            print(self.form_data)

            return {
                'years': years,
                'counties': counties,
                'units': unit_list
            }
        else:
            print('fail to get year and county list')
            return None

    def SessionKeepAlive(self):
        self.session.headers['Origin'] = 'https://gateway.ifionline.org'
        self.session.headers['Referer'] = 'https://gateway.ifionline.org/report_builder/Default3a.aspx?rpttype=employComp&rpt=EmployComp&rptName=Employee%20Compensation'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'

        # set get data
        params = {}
        params['OpType'] = 'SessionKeepAlive'
        params['ControlID'] = self.form_data['ControlID']

        # set url
        url = 'https://gateway.ifionline.org/Reserved.ReportViewerWebControl.axd'

        # get request
        ret = self.session.post(url, params=params)

        if ret.status_code == 200:
            print(ret.text)
            return
        else:
            print('fail: SessionKeepAlive')
            return None

    def GetReportingunitList(self, year, county):
        # set get data
        params = {}
        params['rpttype'] = 'employComp'
        params['rpt'] = 'EmployComp'
        params['rptName'] = 'Employee Compensation'

        # set post data
        data = {}
        data['ScriptManager1'] = 'ScriptManager1|ReportViewer1$ctl04$ctl05$ddValue'
        data['ScriptManager1_HiddenField'] = ''
        data['ReportViewer1$ctl03$ctl00'] = ''
        data['ReportViewer1$ctl03$ctl01'] = ''
        data['ReportViewer1$ctl10'] = ''
        data['ReportViewer1$ctl11'] = 'standards'
        data['ReportViewer1$AsyncWait$HiddenCancelField'] = 'False'
        data['ReportViewer1$ctl04$ctl03$ddValue'] = year['value']
        data['ReportViewer1$ctl04$ctl05$ddValue'] = county['value']
        data['ReportViewer1$ctl04$ctl07$ddValue'] = '0'
        data['ReportViewer1$ToggleParam$store'] = ''
        data['ReportViewer1$ToggleParam$collapse'] = 'false'
        data['ReportViewer1$ctl08$ClientClickedId'] = ''
        data['ReportViewer1$ctl07$store'] = ''
        data['ReportViewer1$ctl07$collapse'] = 'false'
        data['ReportViewer1$ctl09$VisibilityState$ctl00'] = 'None'
        data['ReportViewer1$ctl09$ScrollPosition'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl02'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl03'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl04'] = '100'
        data['__EVENTTARGET'] = 'ReportViewer1$ctl04$ctl05$ddValue'
        data['__EVENTARGUMENT'] = ''
        data['__LASTFOCUS'] = ''
        data['__VIEWSTATE'] = self.form_data['__VIEWSTATE']
        data['__VIEWSTATEGENERATOR'] = self.form_data['__VIEWSTATEGENERATOR']
        data['__SCROLLPOSITIONX'] = '0'
        data['__SCROLLPOSITIONY'] = '0'
        data['__EVENTVALIDATION'] = self.form_data['__EVENTVALIDATION']
        data['__ASYNCPOST'] = 'true'

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, params=params, data=data)

        if ret.status_code == 200:
            # get year list
            unit_list = []
            options = Selector(text=ret.text).xpath('//select[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option').extract()
            for idx in range(1, len(options)):
                unit_list.append({
                    'text': str(Selector(text=options[idx]).xpath('//option/text()').extract()[0]).replace('\xa0', ' '),
                    'value': Selector(text=options[idx]).xpath('//option/@value').extract()[0]
                })
            print(unit_list)

            # print(ret.text)
            return unit_list
        else:
            print('fail to get reporting unit list')
            return None

    def GetViewReport(self, year, county, unit):
        # set get data
        params = {}
        params['rpttype'] = 'employComp'
        params['rpt'] = 'EmployComp'
        params['rptName'] = 'Employee Compensation'

        # set post data
        data = {}
        data['ScriptManager1'] = 'ScriptManager1|ReportViewer1$ctl04$ctl00'
        data['ScriptManager1_HiddenField'] = ''
        data['ReportViewer1$ctl03$ctl00'] = ''
        data['ReportViewer1$ctl03$ctl01'] = ''
        data['ReportViewer1$ctl10'] = 'ltr'
        data['ReportViewer1$ctl11'] = 'standards'
        data['ReportViewer1$AsyncWait$HiddenCancelField'] = 'False'
        data['ReportViewer1$ctl04$ctl03$ddValue'] = year['value']
        data['ReportViewer1$ctl04$ctl05$ddValue'] = county['value']
        data['ReportViewer1$ctl04$ctl07$ddValue'] = unit['value']
        data['ReportViewer1$ToggleParam$store'] = ''
        data['ReportViewer1$ToggleParam$collapse'] = 'false'
        data['ReportViewer1$ctl05$ctl00$CurrentPage'] = 1
        data['ReportViewer1$ctl08$ClientClickedId'] = ''
        data['ReportViewer1$ctl07$store'] = ''
        data['ReportViewer1$ctl07$collapse'] = 'false'
        data['ReportViewer1$ctl09$VisibilityState$ctl00'] = 'None'
        data['ReportViewer1$ctl09$ScrollPosition'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl02'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl03'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl04'] = '100'
        data['__EVENTTARGET'] = ''
        data['__EVENTARGUMENT'] = ''
        data['__LASTFOCUS'] = ''
        data['__VIEWSTATE'] = self.form_data['__VIEWSTATE']
        data['__VIEWSTATEGENERATOR'] = self.form_data['__VIEWSTATEGENERATOR']
        data['__SCROLLPOSITIONX'] = '0'
        data['__SCROLLPOSITIONY'] = '0'
        data['__EVENTVALIDATION'] = self.form_data['__EVENTVALIDATION']
        data['__ASYNCPOST'] = 'true'
        data['ReportViewer1$ctl04$ctl00'] = 'View Report'

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, params=params, data=data)

        if ret.status_code == 200:
            # print(ret.text)
            return
        else:
            print('fail to get view report')
            return None

    def ReservedAsyncLoadTarget(self, year, county, unit):
        # set get data
        params = {}
        params['rpttype'] = 'employComp'
        params['rpt'] = 'EmployComp'
        params['rptName'] = 'Employee Compensation'

        # set post data
        data = {}
        data['ScriptManager1'] = 'ScriptManager1|ReportViewer1$ctl09$Reserved_AsyncLoadTarget'
        data['ScriptManager1_HiddenField'] = ''
        data['ReportViewer1$ctl03$ctl00'] = ''
        data['ReportViewer1$ctl03$ctl01'] = ''
        data['ReportViewer1$ctl10'] = 'ltr'
        data['ReportViewer1$ctl11'] = 'standards'
        data['ReportViewer1$AsyncWait$HiddenCancelField'] = 'False'
        data['ReportViewer1$ctl04$ctl03$ddValue'] = year['value']
        data['ReportViewer1$ctl04$ctl05$ddValue'] = county['value']
        data['ReportViewer1$ctl04$ctl07$ddValue'] = unit['value']
        data['ReportViewer1$ToggleParam$store'] = ''
        data['ReportViewer1$ToggleParam$collapse'] = 'false'
        data['ReportViewer1$ctl05$ctl00$CurrentPage'] = ''
        # data['ReportViewer1$ctl05$ctl03$ctl00'] = ''
        data['ReportViewer1$ctl08$ClientClickedId'] = ''
        data['ReportViewer1$ctl07$store'] = ''
        data['ReportViewer1$ctl07$collapse'] = 'false'
        data['ReportViewer1$ctl09$VisibilityState$ctl00'] = 'None'
        data['ReportViewer1$ctl09$ScrollPosition'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl02'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl03'] = ''
        data['ReportViewer1$ctl09$ReportControl$ctl04'] = '100'
        data['__EVENTTARGET'] = 'ReportViewer1$ctl09$Reserved_AsyncLoadTarget'
        data['__EVENTARGUMENT'] = ''
        data['__LASTFOCUS'] = ''
        data['__VIEWSTATE'] = self.form_data['__VIEWSTATE']
        data['__VIEWSTATEGENERATOR'] = self.form_data['__VIEWSTATEGENERATOR']
        data['__SCROLLPOSITIONX'] = '0'
        data['__SCROLLPOSITIONY'] = '0'
        data['__EVENTVALIDATION'] = self.form_data['__EVENTVALIDATION']
        data['__ASYNCPOST'] = 'true'

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, params=params, data=data)

        if ret.status_code == 200:
            # print(ret.text)
            return
        else:
            print('fail: ReservedAsyncLoadTarget')
            return None

    def GetCsvFile(self, file_name):
        file_name = 'csvs/' + str(file_name).replace('/', '-')

        if os.path.isfile(file_name) == True:
            print('this file already downloaded.')
            return

        # set post data
        params = {}
        params['ReportSession'] = '4no5fs2jlgvipriootnf5f55'
        params['Culture'] = '1033'
        params['CultureOverrides'] = 'True'
        params['UICulture'] = '1033'
        params['UICultureOverrides'] = 'True'
        params['ReportStack'] = '1'
        params['ControlID'] = self.form_data['ControlID']
        params['OpType'] = 'Export'
        params['FileName'] = 'SalarySearch'
        params['ContentDisposition'] = 'OnlyHtmlInline'
        params['Format'] = 'CSV'
        params['unit_id'] = '1'

        # set url
        url = 'https://gateway.ifionline.org/Reserved.ReportViewerWebControl.axd'

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(ret.content)
            print('success to download csv file')
        else:
            print('fail to get csv file')
            return None

    def Start(self):
        # get year and county list
        print('getting year and county list ...')
        temp = self.GetYearAndCountyList()
        year_list = temp['years']
        county_list = temp['counties']
        unit_list = temp['units']

        # flag = False
        for year in year_list:
            for county in county_list:
                # if START_YEAR == year['text'] and START_COUNTY == county['text']: flag = True
                # if flag == False: continue

                if year['value'] == '1' and county['value'] == '1':
                    temp = 0
                else:
                    # get reporting unit list
                    print('getting reporting unit list for %s:%s...' % (year['text'], county['text']))
                    unit_list = self.GetReportingunitList(year, county)

                for unit in unit_list:
                    # get view report
                    print('getting view report for %s:%s:%s...' % (year['text'], county['text'], unit['text']))
                    self.GetViewReport(year, county, unit)

                    # ReservedAsyncLoadTarget
                    print('ReservedAsyncLoadTarget for %s:%s:%s...' % (year['text'], county['text'], unit['text']))
                    self.ReservedAsyncLoadTarget(year, county, unit)

                    file_name = county['text'] + '_' + year['text'] + '_' + unit['text'] + '.csv'
                    self.GetCsvFile(file_name)

            #         break
            #     break
            # break

def WriteHeader(file_name):
    # set headers
    header_info = []
    header_info.append('employee')
    header_info.append('department')
    header_info.append('job_title_duties')
    header_info.append('city')
    header_info.append('compensation')
    header_info.append('year')
    header_info.append('county')
    header_info.append('reporting_unit')

    # write header into output csv file
    writer = csv.writer(open(file_name, 'w'), delimiter=',', lineterminator='\n')
    writer.writerow(header_info)

def WriteData(data, file_name):
    # write data into output csv file
    writer = csv.writer(open(file_name, 'a'), delimiter=',', lineterminator='\n')
    writer.writerow(data)

def MergeCsvFiles():
    # write header for csv files
    WriteHeader('counties.csv')
    WriteHeader('state.csv')

    folder_path = 'csvs/'

    # get file list
    dirs = os.listdir(folder_path)

    # flag = False
    # merge files
    for file in dirs:
        print(file + '...')

        # if file == 'State_2012_Indiana University.csv': flag = True
        # if flag == False: continue

        name_split = str(file).split('_')

        output_file = 'counties.csv'
        if name_split[0] == 'State':
            output_file = 'state.csv'

        county = name_split[0]
        year = name_split[1]
        unit = name_split[2]


        reader = csv.reader(open(folder_path + file, 'r', encoding="utf8"))

        for row in reader:
            if len(row) == 6 and row[0] != 'Textbox6':
                # get data
                data = [
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    year,
                    county,
                    unit
                ]

                # write data into output csv file
                WriteData(data, output_file)

        # break
#------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = IndianaScraper()

    # start to scrape
    scraper.Start()

    MergeCsvFiles()

if __name__ == '__main__':
    main()