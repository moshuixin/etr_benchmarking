from django.conf.urls import url
from etr_benchmarking.views import basic_views as views
from etr_benchmarking.views import predict_views

urlpatterns = [
    url(r'^$',
        views.home,
        name='home'),
    url(r'about/$',
        views.about,
        name='about'),
    url(r'^etr/$', views.etr, name='etr'),
    url(r'^getIndustryDropdownValues/$', views.getIndustryDropdownValues, name='getIndustryDropdownValues'),
    url(r'^getCompanyDropdownValues/$', views.getCompanyDropdownValues, name='getCompanyDropdownValues'),
    url(r'^companyanalysis/$', views.companyAnalysis, name='companyAnalysis'),
    url(r'^etrindex/$', views.etrindex, name='etrindex'),
    url(r'^getYearValues/$', views.getYearValues, name='getYearValues'),
    url(r'^getETRforEachYearforCompanyName/$', views.getETRforEachYearforCompanyName, name='getETRforEachYearforCompanyName'),
    url(r'^getETRforEachYearforPeers/$', views.getETRforEachYearforPeers, name='getETRforEachYearforPeers'),
    url(r'^getReconciliationItems/$', views.getReconciliationItems, name='getReconciliationItems'),
    url(r'^getBubbleChartData/$', views.getBubbleChartData, name='getBubbleChartData'),
    ###########predict##########################
    url(r'^getCompanyForDropdown/$', predict_views.getCompanyForDropdown, name='getCompanyForDropdown'),
    url(r'^getIndustryForAllCompany/$', predict_views.getIndustryForAllCompany, name='getIndustryForAllCompany'),
    url(r'^getValuesForPredict/$', predict_views.getValuesForPredict, name='getValuesForPredict'),
]

