from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import pandas as pd
from pandas.tseries.offsets import *
import numpy as np
from sklearn  import datasets, linear_model

import json
import math
import csv

@login_required
def home(request):
    """
    Renders the home page.

    :param request: HttpRequest: Standard httprequest from Django
    :return: rendering of the page
    """
    assert isinstance(request, HttpRequest)

    return render(request, 'etr_benchmarking/etrindex.html')

@login_required
def about(request):
    return render(request, 'predictETR/home.html',{"title":"About"})


@login_required
def etr(request):
    df = pd.DataFrame([[1, 2, 3], [1, 2, 4], [4, 3, 5]])
    context = {
        'title': 'Plots',
        'message': 'Your application description page.',
        'data': df.to_json(orient='values')
    }
    return render(request, 'etr_benchmarking/ETRoverview.html', context)


@ensure_csrf_cookie
def getIndustryDropdownValues(request):
    industryList = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    df = xl.parse("2016")
    for index, row in df.iterrows():
        entry = str(row[df.columns[2]]).replace('\t', '').replace('\n', '')
        if entry != 'nan':
            industryList.append(entry)

    # industryList.remove('nan')
    industryList = list(set(industryList))
    industryList.sort()

    # print(industryList)
    return HttpResponse(json.dumps({"industryList": industryList}), content_type='application/json')


@ensure_csrf_cookie
def getCompanyDropdownValues(request):
    companyList = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    df = xl.parse("2016")
    for index, row in df.iterrows():
        entry = str(row[df.columns[0]]).replace('\t', '').replace('\n', '')
        if entry != 'nan':
            companyList.append(entry)

    # industryList.remove('nan')
    companyList = list(set(companyList))
    companyList.sort()

    # print(companyList)
    return HttpResponse(json.dumps({"companyList": companyList}), content_type='application/json')


def etrindex(request):
    return render(request, 'etr_benchmarking/etrindex.html')


@login_required
def companyAnalysis(request):
    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    # turn sheets into dataframe
    df2016 = xl.parse("2016")
    df2015 = xl.parse("2015")
    df2014 = xl.parse("2014")

    eyLabel = df2016.ix[1][4:56]

    for index, row in df2016.iterrows():
        entry = str(row[df2016.columns[0]]).replace('\t', '').replace('\n', '')
        if entry != 'nan' and entry == 'COCA COLA CO':
            etrvalue2016 = row[df2016.columns[3]] * 100
            # values of the reconciliation items 2016 of related company
            reconItem2016 = pd.Series(row[df2016.columns[4:56]].values, index=eyLabel.values)

    for index, row in df2015.iterrows():
        entry = str(row[df2015.columns[0]]).replace('\t', '').replace('\n', '')
        if entry != 'nan' and entry == 'COCA COLA CO':
            etrvalue2015 = row[df2015.columns[3]] * 100
            # values of the reconciliation items 2015 of related company
            reconItem2015 = pd.Series(row[df2015.columns[4:56]].values, index=eyLabel.values)

    for index, row in df2014.iterrows():
        entry = str(row[df2014.columns[0]]).replace('\t', '').replace('\n', '')
        if entry != 'nan' and entry == 'COCA COLA CO':
            etrvalue2014 = row[df2014.columns[3]] * 100
            # values of the reconciliation items 2014 of related company
            reconItem2014 = pd.Series(row[df2014.columns[4:56]].values, index=eyLabel.values)

    df = pd.DataFrame([[etrvalue2014, etrvalue2015, etrvalue2016]])

    sortedReconItemNotNan2016 = reconItem2016.dropna().sort_values(ascending=False)
    sortedReconItemNotNan2015 = reconItem2015.dropna().sort_values(ascending=False)
    sortedReconItemNotNan2014 = reconItem2014.dropna().sort_values(ascending=False)

    sortedReconItemNotNan1415 = sortedReconItemNotNan2014.add(sortedReconItemNotNan2015, fill_value=0).sort_values(
        ascending=False) / 2
    sortedReconItemNotNan1416 = sortedReconItemNotNan2014.add(sortedReconItemNotNan2016, fill_value=0).sort_values(
        ascending=False) / 2
    sortedReconItemNotNan1516 = sortedReconItemNotNan2015.add(sortedReconItemNotNan2016, fill_value=0).sort_values(
        ascending=False) / 2
    sortedReconItemNotNan141516 = sortedReconItemNotNan2014.add(sortedReconItemNotNan1516 * 2,
                                                                fill_value=0).sort_values(ascending=False) / 3

    context = {
        'title': 'Your ETR',
        'data': df.to_json(orient='values'),
        'recon2016': sortedReconItemNotNan2016.to_json(orient='index'),
        'recon2015': sortedReconItemNotNan2015.to_json(orient='index'),
        'recon2014': sortedReconItemNotNan2014.to_json(orient='index'),
        'recon2014': sortedReconItemNotNan2014.to_json(orient='index'),
        'recon1415': sortedReconItemNotNan1415.to_json(orient='index'),
        'recon1416': sortedReconItemNotNan1416.to_json(orient='index'),
        'recon1516': sortedReconItemNotNan1516.to_json(orient='index'),
        'recon141516': sortedReconItemNotNan141516.to_json(orient='index')

    }

    return render(request, 'etr_benchmarking/companyAnalysis.html', context)


@login_required
def vis(request):
    df = pd.DataFrame([[1, 2, 3, 2, 1, 2], [1, 2, 4, 8, 16, 32], [4, 3, 5, 9, 8, 7]])
    # print(df)
    context = {
        'title': 'Vis.js',
        'message': 'Your application description page.',
        'data': df.to_json(orient='values')
    }
    return render(request, 'etr_benchmarking/vis.html', context)


@login_required
def countrymap(request):
    context = {'title': 'Country Map'}
    return render(request, 'etr_benchmarking/countrymap.html', context)


@login_required
def leaflet(request):
    context = {'title': 'Leaflet / OpenStreetMap'}
    return render(request, 'etr_benchmarking/leaflet.html', context)


@login_required
def icons(request):
    context = {'title': 'Icons'}
    return render(request, 'etr_benchmarking/icons.html', context)


@login_required
def notifications(request):
    context = {'title': 'Notifications'}
    return render(request, 'etr_benchmarking/notifications.html', context)


@login_required
def panel_wells(request):
    context = {'title': 'Panels and Wells'}
    return render(request, 'etr_benchmarking/panels-wells.html', context)


@login_required
def tables(request):
    context = {'title': 'Tables'}
    return render(request, 'etr_benchmarking/tables.html', context)


@login_required
def typography(request):
    context = {'title': 'Typography'}
    return render(request, 'etr_benchmarking/typography.html', context)


@ensure_csrf_cookie
def getBubbleChartData(request):
    companyName = request.POST.get('companyName')
    companies = request.POST.getlist('companies[]')
    industries = request.POST.getlist('industries[]')
    years = request.POST.getlist('years[]')
    # print(companies)
    # print(years)
    # print(industries)
    BubbleChartData = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    for sheetname in xl.sheet_names:
        if sheetname.isdigit() and sheetname in years:  # year
            df = xl.parse(sheetname, skiprows=3)
            for index, row in df.iterrows():
                company = str(row[0]).replace('\t', '').replace('\n', '')
                industry = str(row[2]).replace('\t', '').replace('\n', '')
                if company != 'nan' and industry != 'nan' and (company in companies or industry in industries):
                    value = float(row[3])
                    value2 = round(value, 3)
                    if not math.isnan(value):
                        BubbleChartData.append([sheetname, company, industry, value])
    # yearList = list(set(yearList))  # uniques
    # yearList.sort()
    BubbleChartData.sort()
    # print(BubbleChartData)
    return HttpResponse(json.dumps({"bubbleChartData": BubbleChartData}), content_type='application/json')


@ensure_csrf_cookie
def getReconciliationItems(request):
    companyName = request.POST.get('companyName')
    # print(companyName)
    reconciliationItems = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    ETRSum = 0
    companyCnt = 0

    for sheetname in xl.sheet_names:
        if sheetname.isdigit():  # year
            df = xl.parse(sheetname)

            for index, row in df.iterrows():
                entry = str(row[0]).replace('\t', '').replace('\n', '')
                if entry != 'nan' and entry == companyName:
                    # value = str(row[df.iloc[index]]).replace('\t', '').replace('\n', '')
                    # for i in range(len(df.columns)):
                    for i in range(4, 56):
                        value = str(row.ix[i]).replace('\t', '').replace('\n', '')
                        EYlabel = str(df.iloc[1, i]).replace('\t', '').replace('\n', '')
                        if i > 0 and value != 'nan' and EYlabel != 'nan':
                            reconciliationItems.append([sheetname, EYlabel, value])
                            # if not math.isnan(value):
                            # print("value")
                            # print(value)
                            # print("name ")
                            # print(df.iloc[1, 5])

    recon2014sum = 0
    recon2015sum = 0
    recon2016sum = 0

    for iter in reconciliationItems:
        if iter[0] == "2014":
            recon2014sum = recon2014sum + abs(float(iter[2]))
        if iter[0] == '2015':
            recon2015sum = recon2015sum + abs(float(iter[2]))
        if iter[0] == '2016':
            recon2016sum = recon2016sum + abs(float(iter[2]))
            #

    # print(recon2014sum, recon2015sum, recon2016sum)
    # yearList = list(set(yearList))  # uniques
    # yearList.sort()
    reconciliationItems.sort()

    context = {
        'reconciliationItems': reconciliationItems,
        'recon2014sum': recon2014sum,
        'recon2015sum': recon2015sum,
        'recon2016sum': recon2016sum,
    }

    # print(reconciliationItems)
    # return HttpResponse(json.dumps({"reconciliationItems": reconciliationItems}), content_type='application/json')
    # return HttpResponse(json.dumps({"reconciliationItems": reconciliationItems},{"recon2014sum": recon2014sum},{"recon2015sum": recon2015sum},{"recon2016sum":recon2016sum}), content_type='application/json')
    return HttpResponse(json.dumps(context), content_type='application/json')


@ensure_csrf_cookie
def getETRforEachYearforCompanyName(request):
    companyName = request.POST.get('companyName')
    # print(companyName)
    ETRHistory = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    for sheetname in xl.sheet_names:
        if sheetname.isdigit():  # year
            df = xl.parse(sheetname, skiprows=3)
            for index, row in df.iterrows():
                entry = str(row[0]).replace('\t', '').replace('\n', '')
                if entry != 'nan' and entry == companyName:
                    value = str(row[3]).replace('\t', '').replace('\n', '')
                    value100 = round(float(value) * 100, 2)
                    ETRHistory.append([sheetname, value100])
                    break

    # yearList = list(set(yearList))  # uniques
    # yearList.sort()
    ETRHistory.sort()
    # print(ETRHistory)
    return HttpResponse(json.dumps({"ETRHistory": ETRHistory}), content_type='application/json')


@ensure_csrf_cookie
def getETRforEachYearforPeers(request):
    companyName = request.POST.get('companyName')
    # print(companyName)
    ETRHistory = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    ETRSum = 0
    companyCnt = 0

    for sheetname in xl.sheet_names:
        if sheetname.isdigit():  # year
            df = xl.parse(sheetname, skiprows=3)
            ETRSum = 0
            companyCnt = 0
            for index, row in df.iterrows():
                entry = str(row[0]).replace('\t', '').replace('\n', '')
                if entry != 'nan' and entry != companyName:
                    value = float(row[3])

                    if not math.isnan(value):
                        # print(value)
                        ETRSum += float(value)
                        companyCnt += 1

            ETRAvg = round(ETRSum / companyCnt, 2)
            ETRAvg100 = float(ETRAvg) * 100
            ETRHistory.append([sheetname, ETRAvg100])

    # yearList = list(set(yearList))  # uniques
    # yearList.sort()
    ETRHistory.sort()
    # print(ETRHistory)
    return HttpResponse(json.dumps({"ETRHistory": ETRHistory}), content_type='application/json')


@ensure_csrf_cookie
def getYearValues(request):
    yearList = []

    xl = pd.ExcelFile('etr_benchmarking/static/ttaa_examples/data/20170516_ETRmapping_with_Amount.xlsx')

    for sheetname in xl.sheet_names:
        if sheetname.isdigit():  # year
            yearList.append(sheetname)

    yearList = list(set(yearList))  # uniques
    yearList.sort()
    return HttpResponse(json.dumps({"yearList": yearList}), content_type='application/json')


    