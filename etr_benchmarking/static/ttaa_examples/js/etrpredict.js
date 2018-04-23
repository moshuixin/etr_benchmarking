// predict the ETR
function companychoose() {
    if (document.getElementById('companyDropdown1').value != "All") {
        document.getElementById('industryDropdown_pre').style.display = 'block';
        
    } else document.getElementById('industryDropdown_pre').style.display = 'block';
}

$('#etr_page').scroll(function() {
    $('#plot_chart').css('top', $(this).scrollTop());
});

//
function getCompanyForDropdown(){
    $.ajax({
        type: "POST",
        url: '../getCompanyForDropdown/',
        data: {  },
        dataType: 'json',
        success: function (response){
    
            var companyList = response.infoList;
            $('#companyDropdown1').empty();

    
            for (var i = 0; i < response.companyList.length; i++){
    
                $('#companyDropdown1').append('<option>'+response.companyList[i]+'</option>');
            }
                $('#companyDropdown1').append('<option>All</option>');
        },
        error: function(xhr, ajaxOptions, thrownError){
        }
        });
        var companyselected = $('#companyDropdown1').val();
        getIndustryForAllCompany(companyselected)
};

//click company drop down
$('#companyDropdown1').on('change',function(){

    var selectedCompany_pre = $('#companyDropdown1 option:selected').val();
    var industryselected = $('#industryDropdown_pre').text();
    console.log(selectedCompany_pre,industryselected,'company change')
    getIndustryForAllCompany(selectedCompany_pre, industryselected);
    
});

function getIndustryForAllCompany(selectedCompany_pre){
    // alert(selectedCompany_pre)
    $.ajax({
        type: "POST",
        url: '../getIndustryForAllCompany/',
        data: { selectedCompany_pre: selectedCompany_pre },
        dataType: 'json',
        success: function (response){
            // console.log(response.industrylist)
            var industrylist = response.industrylist;
            $('#industryDropdown_pre').empty();
            // console.log(response.industrylist.length)
            if (response.industrylist.length<2){
                for (var i = 0; i < response.industrylist.length; i++){
        
                    $('#industryDropdown_pre').append('<option>'+response.industrylist[i]+'</option>');
                }

                }
            else{
                for (var i = 0; i < response.industrylist.length; i++){
        
                    $('#industryDropdown_pre').append('<option>'+response.industrylist[i]+'</option>');
                }
                    $('#industryDropdown_pre').append('<option>All</option>');
            }
        },
        error: function(xhr, ajaxOptions, thrownError){
            //   alert(ajaxOptions);
        }
        });
        
        var companyselected = $('#companyDropdown1 option:selected').val();
        var industryselected = $('#industryDropdown_pre').val();
        console.log(companyselected,industryselected)
        getValuesForPredict(companyselected,industryselected)
};

//click industry drop down
$('#industryDropdown_pre').on('change',function(){
    var companyselected = $('#companyDropdown1 ').val();
    var industryselected = $('#industryDropdown_pre option:selected').val();
    console.log(companyselected,industryselected,'industry change')
    getValuesForPredict(companyselected,industryselected);
    
});

// slider move, get values
$('#statutory, #foreign, #state ,#credit,#nondeductible,#deductions, #settlement,#contingency,#other,#sliderEBT').change(function() {    
            $('.range-slider').on('change', '.range-slider__range', function(){
                $(this).parent().find('.Value').html (" " + this.value + " Mio"); 
            });
});


// get the values from views
function getValuesForPredict(companyselected,industryselected){ 
    $.ajax({
        type: "POST",
        url: '../getValuesForPredict/',
        data: { companyselected:companyselected,industryselected:industryselected},
        dataType: 'json',
        success: function (response){
            console.log(response.infoList)
            drawchart(response.infoList)
    }    
    });
    
};

// draw plot
function drawchart(ETR){

            console.log(ETR)
            var ETRs = [];
            var years = [];
            var chartColors = [];
            var statutory = parseInt($('#statutory').val());
            var foreign = parseInt($('#foreign').val());
            var state = parseInt($('#state').val());
            var credit = parseInt($('#credit').val());
            var nondeductible = parseInt($('#nondeductible').val());
            var settlement = parseInt($('#settlement').val());
            var contingency = parseInt($('#contingency').val());
            var other = parseInt($('#other').val());
            var sliderEBT = parseInt($('#sliderEBT').val());
            var etr_target = (statutory+foreign +state+ credit+nondeductible+settlement+contingency+other)/sliderEBT
            console.log(etr_target);

            for (var i = 0; i < ETR.length-1; i++){ //all years except last (highest) one
                ETRs.push(ETR[i]);
                console.log(ETRs)
               
                
                chartColors.push('grey');
            }
            years.push('2012','2013','2014','2015','2016');
            ETRs.push(ETR[5]); //forecasted etr in views.py to calculate this value

            
            years.push('2017_predict');//
            ETRs.push(etr_target);
            years.push("2017_target")
            chartColors.push('yellow');
            $('#chartContainer1').empty();
            $('#chartContainer1').append('<canvas id="ETRChart1"></canvas>');
            var ctx = document.getElementById("ETRChart1").getContext("2d");
            var etrChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: years,
                    datasets: [{
                        label:'ETR',
                        data: ETRs,
                        backgroundColor: chartColors,
                        borderColor: 'yellow',
                    }]
                },
                options: {
                    
                    scales: {
                        xAxes: [{
                            ticks: {
                                fontSize: 13
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'year'
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                fontSize: 13
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'ETR'
                            }
                        }]
                    },
                }
            });
    
    
};
