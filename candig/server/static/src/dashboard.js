"use strict";

$(window).on('load', function() {

    makeRequest("datasets/search", {}).then(function(response) {

        const data = JSON.parse(response);
        const listOfDatasetId = data['results']['datasets'];

        let dropdown = document.getElementById("dropdown-menu");

        for (let i = 0; i < listOfDatasetId.length; i++) {
            if (!finalDatasetId.includes(listOfDatasetId[i]['id'])) {
                finalDatasetId.push(listOfDatasetId[i]['id']);
                finalDatasetName.push(listOfDatasetId[i]['name']);
            }
        }

        for (let j = 0; j < finalDatasetId.length; j++) {
            dropdown.innerHTML += '<a class="dropdown-item" id="refresh" href="javascript:void(0)" onclick="refreshDataset(' + j + ')">' + finalDatasetName[j] + '</a>'
        }

        // If the cookie is not set; or if it is set, but not in a list of available datasets
        if (getCookie("datasetId") == null || finalDatasetId.indexOf(getCookie("datasetId")) == -1) {
            datasetId = finalDatasetId[0];
            setCookie("datasetId", datasetId);
            $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[0]);
        } else {
            datasetId = getCookie("datasetId");
            $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(datasetId)]);
        }

        let dashboard_instance = new dashboard();
        dashboard_instance.initialize();

    }, function(Error) {
        alertBuilder("No datasets currently available. Please contact a system administrator for assistance.");
        noPermissionMessageMultiple(["queryStatus", "responseToTreatment", "therapeuticToResponses", "cancerTypes", "drugScatter", "hospitals", "timelineSamples"]);
    })
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    document.getElementById("warningMsg").style.display = "none";
    setCookie("datasetId", datasetId);
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
    let dashboard_instance = new dashboard();
    dashboard_instance.initialize();
}


function dashboard() {
    var treatments;

    this.initialize = function() {
        alertCloser();
        loadingBarInitiator();
        enrollmentsFetcher();

        countRequest("treatments", 
            ["responseToTreatment", "therapeuticModality"], 
            datasetId
        ).then(function(data) {
            server_status_update(JSON.parse(data));

            let response = JSON.parse(data)["results"]["treatments"][0];
            singleLayerDrawer("responseToTreatment", 'bar', 'Response to treatments', response["responseToTreatment"]);
            singleLayerDrawer("therapeuticToResponses", 'bar', 'Therapeutic Types', response["therapeuticModality"]);
        })

        countRequest("diagnoses", ["cancerType"], datasetId).then(function(data) {
            let response = JSON.parse(data)["results"]["diagnoses"][0];
            cancerTypeDrawer('cancerTypes', "pie", "Cancer types and corresponding treatment drugs", response["cancerType"]);

            // Render a random drug frequence plot on load
            if (response["cancerType"]) {
                let listOfCancerTypes = Object.keys(response["cancerType"]);
                var selectedCancerType = listOfCancerTypes[Math.floor(Math.random() * listOfCancerTypes.length)];
                drugScatter(selectedCancerType);
            }
            else noPermissionMessage("drugScatter");
        })

    }

    function loadingBarInitiator() {
        let loader = '<div class="loader_bar"></div>'
        document.getElementById("responseToTreatment").innerHTML = loader;
        document.getElementById("therapeuticToResponses").innerHTML = loader;
        document.getElementById("cancerTypes").innerHTML = loader;
        document.getElementById("drugScatter").innerHTML = loader;
        document.getElementById("hospitals").innerHTML = loader;
        document.getElementById("queryStatus").innerHTML = loader;
        document.getElementById("timelineSamples").innerHTML = loader;
    }

    function enrollmentsFetcher() {
        makeRequest("enrollments/search", {
            "datasetId": datasetId
        }).then(function(response) {
            var data = JSON.parse(response);

            var sampleDataset = data['results']['enrollments'];
            var collectionDateArray = [];
            var hospitalFrequency;

            hospitalFrequency = groupBy(sampleDataset, "treatingCentreName")

            if (Object.keys(hospitalFrequency).length == 0) {
            	noPermissionMessage("hospitals")
            }
            else singleLayerDrawer("hospitals", 'bar', 'Hospital distribution', hospitalFrequency);

            if (sampleDataset[0]["enrollmentApprovalDate"] == undefined) {
                noPermissionMessage("timelineSamples");
            } else {
                for (var i = 0; i < sampleDataset.length; i++) {
                    if (sampleDataset[i]['enrollmentApprovalDate']) {
                        let tempDate = new Date(sampleDataset[i]['enrollmentApprovalDate']);
                        sampleDataset[i]['enrollmentApprovalDate'] = tempDate.getFullYear();
                    }
                }

                collectionDateArray = groupBy(sampleDataset, "enrollmentApprovalDate")

                var years = Object.keys(collectionDateArray);
                var yearsCount = Object.values(collectionDateArray);

                var cumulativeYearCounts = [0];

                yearsCount.forEach(function(elementToAdd, index) {
                    var newElement = cumulativeYearCounts[index] + elementToAdd;
                    cumulativeYearCounts.push(newElement);
                });
                cumulativeYearCounts.shift();

                timelineDrawer(yearsCount, years, cumulativeYearCounts);
            }
        }, function(Error) {
                noPermissionMessageMultiple(['hospitals', 'timelineSamples']);
        })
    }

    // This function calculates the cumulative sum over the years
    function timelineDrawer(yearsCount, years, cumulativeData) {
        Highcharts.chart('timelineSamples', {
            chart: {
                type: 'area',
                zoomType: 'xy',
                style: {
                    fontFamily: "Roboto"
                }
            },
            title: {
                text: 'Samples received by years'
            },
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: years,
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: ''
                },
                labels: {
                    formatter: function() {
                        return this.value;
                    }
                }
            },
            tooltip: {
                split: true,
                valueSuffix: ''
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666'
                    }
                }
            },
            series: [{
                type: 'column',
                name: 'new sample',
                data: yearsCount
            }, {
                type: 'line',
                name: 'Cumulative samples',
                data: cumulativeData
            }]
        });
    }

    function server_status_update(data) {

        var statusObj = {
            "Known Peers": data['status']['Known peers'],
            "Queried Peers": data['status']['Queried peers'],
            "Successful Communications": data['status']['Successful communications']
        }

        singleLayerDrawer("queryStatus", 'bar', 'Server status', statusObj);
    }


    // Draw the drug scatter plot
    function drugScatter(cancerType) {

        let listOfDrugsWithLength = {}

        // Format: [[0, y1], [0, y2], [1, y3] ...] to render the scatter plot.
        let indexedDrugList = []
        let day = 1000 * 60 * 60 * 24

        searchRequest("diagnoses", ["systematicTherapyAgentName", "startDate", "stopDate"], datasetId, 
            {"field": "cancerType", "operator": "==", "value": cancerType}, "chemotherapies").then(function (response){

            if (response.length == 0) {
            	noPermissionMessage("drugScatter");
            }

            else {
	            for (let i = 0; i < response.length; i++) {
	                let curr = response[i]
                    let duration;
                    let pattern = /\d{1,4}[/-]\d{1,2}[/-]\d{1,2}/;


                    if (curr["startDate"].match(pattern) == null && curr["stopDate"].match(pattern) == null) {
                        try {
                            duration = parseInt(curr["stopDate"]) - parseInt(curr["startDate"]);
                        }
                        catch (err) {
                            // exit current iteration
                            continue;
                        }
                    }

                    else {
                        let startDate = new Date(curr["startDate"]);
                        let stopDate = new Date(curr["stopDate"]);
                        duration = Math.floor((stopDate - startDate) / day);                        
                    }

	                let drug = curr["systematicTherapyAgentName"]

	                if (!listOfDrugsWithLength[drug]) {
	                   listOfDrugsWithLength[drug] = [];
	                   listOfDrugsWithLength[drug].push(duration);
	                }
	                else listOfDrugsWithLength[drug].push(duration);
	            }

	        	let drugList = Object.keys(listOfDrugsWithLength);

	            for (let i = 0; i < drugList.length; i++) {

	            	for (let j = 0; j < listOfDrugsWithLength[drugList[i]].length; j++) {
	            		let tempDrugDate = [];
	            		tempDrugDate.push(i);
	            		tempDrugDate.push(listOfDrugsWithLength[drugList[i]][j]);
	            		indexedDrugList.push(tempDrugDate);
	            	}
	            }

		        Highcharts.chart("drugScatter", {
		            chart: {
		                renderTo: 'drugScatter',
		                type: 'scatter',
		                zoomType: 'xy',
                        style: {
                            fontFamily: "Roboto"
                        }
		            },
		            title: {
		                text: 'Time of drug treatment for ' + cancerType
		            },
		            credits: {
		                enabled: false
		            },
		            exporting: {
		                enabled: false
		            },
		            xAxis: {
		                categories: drugList
		            },
		            yAxis: {
		                title: {
		                    text: 'days'
		                }
		            },
		            tooltip: {
		                formatter: function() {
		                    return '' +
		                        this.x + ', ' + this.y + ' days';
		                }
		            },
		            plotOptions: {
		                scatter: {
		                    marker: {
		                        symbol: 'circle',
		                        radius: 5,
		                        states: {
		                            hover: {
		                                enabled: true,
		                                lineColor: 'rgb(100,100,100)'
		                            }
		                        }
		                    },
		                    states: {
		                        hover: {
		                            marker: {
		                                enabled: false
		                            }
		                        }
		                    }
		                }
		            },
		            series: [{
		                name: 'Drugs',
		                color: 'rgba(223, 83, 83, .75)',
		                data: indexedDrugList

		            }]
		        });
            }

        })
    }

    function cancerTypeDrawer(id, type, title, count) {
    	if (count == undefined) {
        	noPermissionMessage(id);
    	}

    	else {
	        var categories = Object.keys(count);
	        var values = Object.values(count);
	        var seriesArray = highChartSeriesObjectMaker(categories, values);

	        Highcharts.chart(id, {
	            chart: {
	                type: type,
                    style: {
                        fontFamily: "Roboto"
                    }
	            },
	            credits: {
	                enabled: false
	            },
	            exporting: {
	                enabled: false
	            },
	            title: {
	                text: title
	            },
	            xAxis: {
	                type: 'category'
	            },
	            legend: {
	                enabled: false
	            },
	            plotOptions: {
	                series: {
	                    borderWidth: 0,
	                    dataLabels: {
	                        enabled: true
	                    }
	                }
	            },
	            series: [{
	                name: 'count',
	                colorByPoint: true,
	                data: seriesArray,
	                cursor: 'pointer',
	                point:{
	                  events:{
	                      click: function (event) {
	                          drugScatter(this.name);
	                      }
	                  }
	              }
	            }]
	        });
    	}
    }

}
