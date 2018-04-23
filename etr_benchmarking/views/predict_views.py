from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import pandas as pd
import numpy as np
from sklearn  import linear_model

import json
import csv

def loaddata_pd():
    """
    using pandas to load the data
    :return: five features' values (numpy array)
    """
    dataset = pd.read_csv('etr_benchmarking/static/ttaa_examples/data/filterdata.csv', encoding='SHIFT-JIS', sep=";",
                          low_memory=False)
    companynames = dataset.iloc[:, 0].values
    industry = dataset.iloc[:, 2].values
    year = dataset.iloc[:, 3].values
    etr = dataset.iloc[:, 4].values
    ITE = dataset.iloc[:, 26].values
    EBT = dataset.iloc[:, 8].values
    print(type(EBT))
    return companynames, industry, year, etr, ITE, EBT


def load_data():
    """
    load the csv file, skip the first line
    :return: list
    """
    with open('etr_benchmarking/static/ttaa_examples/data/filterdata.csv', 'rt') as file:
        next(file)
        transactions = list(csv.reader(file, delimiter=';'))
    return transactions


@ensure_csrf_cookie
def getCompanyForDropdown(request):
    """
    :param request: HttpRequest: Standard httprequest from Django
    :return: rendering of company for loading dropdown
    """
    companynames, industry, year, etr, ITE, EBT = loaddata_pd()
    companyList = list(set(companynames))
    return HttpResponse(json.dumps({"companyList": companyList}), content_type='application/json')


@ensure_csrf_cookie
def getIndustryForAllCompany(request):
    """
    :param request:
    :return:
    """
    company = request.POST.get('selectedCompany_pre')

    industrylist = []
    companynames, industry, year, etr, ITE, EBT = loaddata_pd()
    transactions = load_data()
    if company == 'All':
        industrylist = list(set(industry))
    else:
        for transaction in transactions:
            if transaction[0] == company:
                industry = transaction[2]
                if industry not in industrylist:
                    industrylist.append(industry)
    return HttpResponse(json.dumps({"industrylist": industrylist}), content_type='application/json')


@ensure_csrf_cookie
def getValuesForPredict(request):
    """
    this function is for predict the etr
    :param request:
    :return:
    """
    companyName = request.POST.get('companyselected')
    industryName = request.POST.get('industryselected')
    infoList = []
    year12 = []
    year13 = []
    year14 = []
    year15 = []
    year16 = []

    transactions = load_data()

    for transaction in transactions:
        name = transaction[0]  # name
        etr = transaction[4]  # etr
        year = transaction[3]  # year
        industry = transaction[2]  # industry
        if transaction[0] == companyName:  # and transaction[2] == industryName:
            infoList.append([year, etr, industry])  # year/etr

        elif companyName == 'All' and industryName == 'All':
            infoList.append([year, etr, industry])

        elif companyName == 'All' and transaction[2] == industryName:
            infoList.append([year, etr, industry])  # year/etr

        else:
            pass
    ################
    # PREDICTION   #
    ################
    for i in range(0, len(infoList)):
        if infoList[i][0] == '2012':
            etr2012 = infoList[i][1]
            year12.append(etr2012)

        elif infoList[i][0] == '2013':
            etr2013 = infoList[i][1]
            year13.append(etr2013)

        elif infoList[i][0] == '2014':
            etr2014 = infoList[i][1]
            year14.append(etr2014)

        elif infoList[i][0] == '2015':
            etr2015 = infoList[i][1]
            year15.append(etr2015)

        elif infoList[i][0] == '2016':
            etr2016 = infoList[i][1]
            year16.append(etr2016)

    try:
        sum_2012 = [float(item) for item in year12]
        sum_2013 = [float(item) for item in year13]
        sum_2014 = [float(item) for item in year14]
        sum_2015 = [float(item) for item in year15]
        sum_2016 = [float(item) for item in year16]
    except:
        print('error')
    etr = pd.DataFrame({'2012': pd.Series(sum_2012),
                        '2013': pd.Series(sum_2013),
                        '2014': pd.Series(sum_2014),
                        '2015': pd.Series(sum_2015),
                        '2016': pd.Series(sum_2016)})
    etr.fillna(0, inplace=True)
    # create model, using linear regression
    data = np.asarray(etr)
    reg = linear_model.LinearRegression()
    X, y = data[:, 0:4], data[:, 4]
    reg.fit(X, y)
    pre = reg.predict(X)

    pre_etr = np.mean(pre)
    ETRlist = [np.mean(data[:, 0]),
               np.mean(data[:, 1]),
               np.mean(data[:, 2]),
               np.mean(data[:, 3]),
               np.mean(data[:, 4]),
               pre_etr]
    print(ETRlist)
    return HttpResponse(json.dumps({"infoList": ETRlist}), content_type='application/json')

