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
        alertBuilder("No data currently available. Please contact a system administrator for assistance.")
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
        samplesFetcher();
        makeRequest("treatments/search", {
            "datasetId": datasetId
        }).then(function(response) {
            var data = JSON.parse(response);
            var statusObj = {
                "Known Peers": data['status']['Known peers'],
                "Queried Peers": data['status']['Queried peers'],
                "Successful Communications": data['status']['Successful communications']
            }
            singleLayerDrawer("queryStatus", 'bar', 'Server status', statusObj);
            treatments = data['results']['treatments'];
            if (treatments[0]["responseToTreatment"] != undefined) {
                cancerTypeDruglistFetcher();
                treatmentsFetcher(treatments);
            } else noPermissionMsg();
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

    function noPermissionMsg() {
        let message = "<p class='noPermission'>You don't have access to this data.</p>";
        document.getElementById("responseToTreatment").innerHTML = message;
        document.getElementById("therapeuticToResponses").innerHTML = message;
        document.getElementById("cancerTypes").innerHTML = message;
        document.getElementById("drugScatter").innerHTML = message;
        document.getElementById("hospitals").innerHTML = message;
    }


    function highChartSeriesObjectMaker(nameArray, dataArray) {
        var tempObj = {};
        var seriesObjList = [];
        var tempDataArray = [];
        for (var i = 0; i < nameArray.length; i++) {
            tempObj = {};
            tempObj['name'] = nameArray[i];
            tempObj['y'] = dataArray[i];
            seriesObjList.push(tempObj);
        }
        return seriesObjList;
    }

    function treatmentsFetcher(treatments) {
        singleLayerDrawer("responseToTreatment", 'bar', 'Response to treatments', groupBy(treatments, "responseToTreatment"));
        singleLayerDrawer("therapeuticToResponses", 'bar', 'Therapeutic Types', groupBy(treatments, "therapeuticModality"));
    }

    function samplesFetcher() {
        makeRequest("enrollments/search", {
            "datasetId": datasetId
        }).then(function(response) {
            var data = JSON.parse(response);
            var sampleDataset = data['results']['enrollments'];
            var collectionDateArray = [];
            var hospitalFrequency;

            if (sampleDataset[0]["treatingCentreName"] != undefined) {
                hospitalFrequency = groupBy(sampleDataset, "treatingCentreName")
                singleLayerDrawer("hospitals", 'bar', 'Hospital distribution', hospitalFrequency);
            }

            if (sampleDataset[0]["enrollmentApprovalDate"] == undefined) {
                document.getElementById("timelineSamples").innerHTML = "<p class='noPermission'>You don't have access to this data.</p>";
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
        })
    }

    // This function calculates the cumulative sum over the years
    function timelineDrawer(yearsCount, years, cumulativeData) {
        Highcharts.chart('timelineSamples', {
            chart: {
                type: 'area',
                zoomType: 'xy'
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

    function drillDownDrawer(elementId, titleText, seriesName, seriesList, cancerTypeWithDrug) {
        Highcharts.chart(elementId, {
            chart: {
                type: 'bar'
            },
            title: {
                text: titleText
            },
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
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
                type: 'pie',
                name: seriesName,
                colorByPoint: true,
                data: seriesList,
                cursor: 'pointer',
                point: {
                    events: {
                        click: function() {
                            drugScatter(cancerTypeWithDrug, this.name);
                        }
                    }
                }
            }],
        });
    }

    function cancerTypeDruglistFetcher() {
        makeRequest("diagnoses/search", {
            "datasetId": datasetId
        }).then(function(response) {
            var data = JSON.parse(response);
            var diagnosesDatasets = data['results']['diagnoses'];
            var seriesList = [];
            var seriesObj = {};
            var tempCancerList = [];

            var cancerTypeWithDrug = {}
            var filteredDiagDataset = []

            for (var i = 0; i < diagnosesDatasets.length; i++) {
                // only the record that has both values will be included
                if (diagnosesDatasets[i]['cancerType'] && diagnosesDatasets[i]['patientId']) {
                    filteredDiagDataset.push(diagnosesDatasets[i])
                }
            }

            // A merged array of diagnoses and treatments, with a left join performed
            var mergedData = filteredDiagDataset.map(x => Object.assign(x, treatments.find(y => y.patientId == x.patientId)));

            // Length of a day
            let day = 1000 * 60 * 60 * 24

            /*
            Build a dict that stores cancerType, drug and duration information.
            Format: {"cancerType1": {"drug1": ["duration1", "duration2", ...]}}
            */
            for (let i = 0; i < mergedData.length; i++) {
                let curr = mergedData[i];

                if (curr["drugListOrAgent"] && curr["startDate"] && curr["stopDate"]) {
                    let startDate = new Date(curr["startDate"]);
                    let stopDate = new Date(curr["stopDate"]);
                    let duration = Math.floor((stopDate - startDate) / day);

                    let currDrugList = curr["drugListOrAgent"].split(", ");

                    for (let j = 0; j < currDrugList.length; j++) {
                        if (!cancerTypeWithDrug[curr["cancerType"]]) {
                            cancerTypeWithDrug[curr["cancerType"]] = {}
                        }

                        // If the list that stores duration of drug has not been initialized
                        if (!cancerTypeWithDrug[curr["cancerType"]][currDrugList[j]]) {
                            cancerTypeWithDrug[curr["cancerType"]][currDrugList[j]] = []
                        }
                        cancerTypeWithDrug[curr["cancerType"]][currDrugList[j]].push(duration)
                    }
                }
            }
            var cancerTypes = Object.keys(cancerTypeWithDrug)

            // A random scatter plot is generated at first
            let randomNum = Math.floor(Math.random() * cancerTypes.length);
            let randomCancer = cancerTypes[randomNum];
            drugScatter(cancerTypeWithDrug, randomCancer);

            // Calculate the frequency of cancer types
            var tempCancerObj = groupBy(diagnosesDatasets, "cancerType")
            var cancerTypesList = Object.keys(tempCancerObj);
            var cancerTypeFreq = Object.values(tempCancerObj);

            for (var i = 0; i < cancerTypesList.length; i++) {
                seriesObj = {};
                seriesObj['name'] = cancerTypesList[i];
                seriesObj['y'] = cancerTypeFreq[i];
                seriesObj['drilldown'] = cancerTypesList[i];
                seriesList.push(seriesObj);
            }

            drillDownDrawer('cancerTypes', "cancer types and corresponding treatment drugs", 'cancer types', seriesList, cancerTypeWithDrug);
        })
    }


    // Draw the drug scatter plot
    function drugScatter(cancerTypeWithDrug, cancerType) {
        // list of drugs used in the current cancer type

        let listOfDrugs = Object.keys(cancerTypeWithDrug[cancerType])
        let listOfDrugsWithLength = []

        for (var i = 0; i < listOfDrugs.length; i++) {
            let temp;
            for (var j = 0; j < cancerTypeWithDrug[cancerType][listOfDrugs[i]].length; j++) {
                temp = []
                temp.push(i)
                temp.push(cancerTypeWithDrug[cancerType][listOfDrugs[i]][j])

                listOfDrugsWithLength.push(temp)
            }
        }

        Highcharts.chart("drugScatter", {
            chart: {
                renderTo: 'drugScatter',
                type: 'scatter',
                zoomType: 'xy'
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
                categories: listOfDrugs
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
                data: listOfDrugsWithLength

            }]
        });
    }

    function singleLayerDrawer(id, type, title, count) {
        var categories = Object.keys(count);
        var values = Object.values(count);
        var seriesArray = highChartSeriesObjectMaker(categories, values);

        Highcharts.chart(id, {
            chart: {
                type: type
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
                data: seriesArray
            }]
        });
    }
}
