"use strict";

/*Retrieve a list of datasets and initialize the page*/
$(window).load(function() {
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

        datasetId = finalDatasetId[0];
        $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[0]);

        if (location.hash == "#candig_patients" || location.hash == "#gene_search" || location.hash == "#sample_analysis") {
            $('.nav-tabs a[href="' + location.hash + '"]').tab('show');
        }

        else $('.nav-tabs a[href="#candig"]').tab('show');

    }, function(Error) {
            document.getElementById('tab-content').style.display = "none";
            alertBuilder("No data currently available. Please contact a system administrator for assistance.")
    })
});

function makeRequest(path, body) {
    return new Promise(function(resolve, reject) {
        let results = []
        let key;

        // Initialize the request with empty pageToken
        return repeatRequest("");

        function repeatRequest(pageToken){
            body["pageToken"] = pageToken;

            var xhr = new XMLHttpRequest();
            xhr.open('POST', prepend_path + path, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
            xhr.onload = function() {
                if (xhr.status === 200) {

                    let data = JSON.parse(xhr.response);

                    // If initial request completes the request, resolve with the raw response
                    if (data["results"]["nextPageToken"] == undefined && results.length == 0) {
                        resolve(xhr.response)
                    }

                    // If unsolved, search for the table name in the response
                    if (key == undefined) {
                        let keys = Object.keys(data["results"])

                        for (let i = 0; i < keys.length; i++) {
                            if (keys[i] != "nextPageToken") {
                                key = keys[i];
                            }
                        }
                    }

                    // If nextPageToken is present, save the current response and calls itself
                    if (data["results"]["nextPageToken"]) {
                        results.push.apply(results, data["results"][key]);
                        repeatRequest(data["results"]["nextPageToken"]);
                    }

                    // If nextPageToken is no longer present, resolve with the complete response
                    else {
                        results.push.apply(results, data["results"][key]);
                        data["results"][key] = results
                        resolve(JSON.stringify(data));
                    }
                } else {
                    reject(Error(xhr.response));
                }
            };
            xhr.onerror = function() {
                reject(Error(xhr.response));
            };
            xhr.send(JSON.stringify(body));
        }
})};

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    let currTab = activeTab.href.split('#')[1];
    $('#topTabs a[href="#' + "refreshTab" + '"]').tab('show');
    $('#topTabs a[href="#' + currTab + '"]').tab('show');
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[datasetIndex]);
}

$("a[href='#gene_search']").on('shown.bs.tab', function(e) {
    window.history.pushState("", "Gene Search", "#gene_search");
    activeTab = e.target;

    // If the dataTable is not initialized, statusCode == -1 meaning that the previous response was invalid
    if (document.getElementById('myTable').innerHTML != "" && statusCode != -1) {
        var table = $("#myTable").DataTable();
        table.destroy();
        document.getElementById("myTable").innerHTML = "";
        statusCode = 0;
    }

})

$("a[href='#sample_analysis']").on('shown.bs.tab', function(e) {
    window.history.pushState("", "Sample Analysis", "#sample_analysis");
    activeTab = e.target;

    var tableIds = ["extractions", "alignments", "sequencing", "variantcalling", "fusiondetection", "expressionanalysis"];

    initialize();

    document.getElementById("sampleSearch").addEventListener("click", caller);

    function initialize(){
        for (let i = 0; i < tableIds; i++){
            document.getElementById(tableIds[i].innerHTML = "");
        }

        // If the list of sample Ids have been fetched, don't fetch again
        if (document.getElementById("sampleSelect").value == "") {
            sampleIDsFetcher();
        }
    }

    function caller(){
        var request = document.getElementById("sampleSelect").value;

        for (let i = 0; i < tableIds.length; i++) {
            xhrInitiator(tableIds[i], tableIds[i], request)
        }
    }

    // Initiates XHR calls to different endpoints
    function xhrInitiator(endpoint, element, request) {
        let requestObj = {
            'datasetId': datasetId,
            "filters": [
                {
                    "field": "sampleId",
                    "operator": "==",
                    "value": request
                }
            ]
        }

        makeRequest(endpoint + "/search", requestObj).then(function(response) {
            tableBuilder(JSON.parse(response), endpoint, element);
        })
    }

    function sampleIDsFetcher() {
        makeRequest("samples/search", {"datasetId": datasetId}).then(function(response) {
            var data = JSON.parse(response)["results"]["samples"].sort();
            let sampleSelect = document.getElementById("sampleSelect");

            for (let i = 0; i < data.length; i++){
                if (data[i]["sampleId"] != undefined){
                    sampleSelect.options[sampleSelect.options.length] = new Option(data[i]["sampleId"], data[i]["sampleId"]);
                }
            }
        })
    }

    function tableBuilder(results, endpoint, id) {
        document.getElementById(id).innerHTML = "";
        var dataset = results["results"][endpoint];
        var keyList = Object.keys(dataset[0]);
        var columnDefs = [];
        var newHeader;
        var hiddenHeaders = ["id", "datasetId", "name"];

        for (var i = 0; i < keyList.length; i++){
            newHeader = {}

            if (!hiddenHeaders.includes(keyList[i])) {
                columnDefs.push(keyList[i]);
            }
        }

        var newColumnDefs = [{"headerName": endpoint, "field": "field"}, {"headerName": "", "field": "value"}];

        for (var k = 0; k < dataset.length; k++) {

            var newDataset = [];

            for (var j = 0; j < columnDefs.length; j++) {
                var tempItem = {};
                tempItem["field"] = columnDefs[j].replace(/([a-z])([A-Z])/g, '$1 $2');
                tempItem["value"] = dataset[k][columnDefs[j]];
                newDataset.push(tempItem);
            }
            gridMaker(newColumnDefs, newDataset, id);
        }
    }

    function gridMaker(newColumnDefs, newDataset, id){

        var gridOptions = {
            domLayout: 'autoHeight',
            columnDefs: newColumnDefs,
            rowData: newDataset,
            enableSorting: true,
            enableFilter: true,
            rowSelection: "multiple",
            defaultColDef: {
            width: 120,
            editable: true,
            filter: 'agTextColumnFilter',
            },
            enableColResize: true
        };

        var eGridDiv = document.querySelector('#' + id);
        new agGrid.Grid(eGridDiv, gridOptions);
    }
})

/*
The following chunk of function gets executed on load, or once the candig tab is selected
*/

$("a[href='#candig']").on('shown.bs.tab', function(e) {
    window.history.pushState("", "HomePage", "/");

    activeTab = e.target;
    var treatments;

    makeRequest("treatments/search", {"datasetId": datasetId}).then(function(response) {
        var data = JSON.parse(response);
        var knownPeers = data['status']['Known peers'];
        var queriedPeers = data['status']['Queried peers'];
        var success = data['status']['Successful communications'];
        var queryStatusSeriesArray = highChartSeriesObjectMaker(["Known Peers", "Queried Peers", "Successful Communications"], [knownPeers, queriedPeers, success]);
        singleLayerDrawer("queryStatus", 'bar', 'Server status', queryStatusSeriesArray);

        samplesFetcher();

        cancerTypeDruglistFetcher();
        treatments = data['results']['treatments'];
        treatmentsFetcher(treatments);
    })

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

    function freqCounter(arrayToCount) {
        let result = {};

        for (var j = 0; j < arrayToCount.length; j++) {
            if (!result[arrayToCount[j]]) {
                result[arrayToCount[j]] = 0;
            }
            ++result[arrayToCount[j]];
        }

        return result;
    }


    function treatmentsFetcher(treatments) {

        var responseArray = [];
        var therapeuticArray = [];

        for (var i = 0; i < treatments.length; i++) {

            if (treatments[i]['responseToTreatment'] != undefined) {
                responseArray.push(treatments[i]['responseToTreatment']);
            }

            if (treatments[i]['therapeuticModality'] != undefined) {
                therapeuticArray.push(treatments[i]['therapeuticModality']);
            }
        }

        var tempCats = Object.keys(freqCounter(responseArray));
        var tempVals = Object.values(freqCounter(responseArray));

        var theraCats = Object.keys(freqCounter(therapeuticArray));
        var theraVals = Object.values(freqCounter(therapeuticArray));

        var treatmentsSeriesArray = highChartSeriesObjectMaker(tempCats, tempVals);
        singleLayerDrawer("responseToTreatment", 'bar', 'Response to treatments', treatmentsSeriesArray);

        var therapeuticSeriesArray = highChartSeriesObjectMaker(theraCats, theraVals);
        singleLayerDrawer("therapeuticToResponses", 'bar', 'Therapeutic Types', therapeuticSeriesArray);
    }

    function samplesFetcher() {
        makeRequest("samples/search", {"datasetId": datasetId}).then(function(response) {
            var data = JSON.parse(response);

            var sampleDataset = data['results']['samples'];
            var tempArray = [];
            var tempDateArray = [];
            var tempObj;
            var misCount;

            for (var i = 0; i < sampleDataset.length; i++) {

                if (sampleDataset[i]['collectionHospital']) {
                    tempArray.push(sampleDataset[i]['collectionHospital']);
                    var tempDate = sampleDataset[i]['collectionDate'];

                    try {
                        var newDate = tempDate.substr(tempDate.length - 4);
                        tempDateArray.push(newDate);
                    } catch (err) {
                        misCount++;
                    }
                }

            }

            tempObj = freqCounter(tempArray);

            var listOfHospitals = Object.keys(tempObj);
            var listOfHospitalNumber = Object.values(tempObj);

            var tempIndex = listOfHospitals.indexOf("undefined");
            if (tempIndex !== -1) {
                listOfHospitals[tempIndex] = 'Other'
            };


            var hospitalNewArray = highChartSeriesObjectMaker(listOfHospitals, listOfHospitalNumber);
            hospitalNewArray.sort(function(a, b) {
                return b.y - a.y
            });
            singleLayerDrawer("hospitals", 'bar', 'Hospital distribution', hospitalNewArray);


            var years = Object.keys(freqCounter(tempDateArray));
            var yearsCount = Object.values(freqCounter(tempDateArray));

            var cumulativeYearCounts = [0];

            yearsCount.forEach(function(elementToAdd, index) {
                var newElement = cumulativeYearCounts[index] + elementToAdd;
                cumulativeYearCounts.push(newElement);
            });
            cumulativeYearCounts.shift();

            timelineDrawer(yearsCount, years, cumulativeYearCounts);
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
        makeRequest("diagnoses/search", {"datasetId": datasetId}).then(function(response) {
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
                    tempCancerList.push(diagnosesDatasets[i]['cancerType']);
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

                if (curr["drugListOrAgent"] && curr["startDate"] && curr["stopDate"]){
                    let startDate = new Date(curr["startDate"]);
                    let stopDate = new Date(curr["stopDate"]);
                    let duration = Math.floor((stopDate - startDate) / day);

                    let currDrugList = curr["drugListOrAgent"].split(", ");

                    for (let j = 0; j < currDrugList.length; j++) {
                        if (!cancerTypeWithDrug[curr["cancerType"]]){
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
            var tempCancerObj = freqCounter(tempCancerList);
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
                        return ''+
                        this.x +', '+ this.y +' days';
                }
            },
            plotOptions: {
                scatter: {
                    marker: {
                        symbol:'circle',
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

    function singleLayerDrawer(id, type, title, seriesArray) {
        Highcharts.chart(id, {
            chart: {
                type: type
            },
            credits: {
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
                name: 'name',
                colorByPoint: true,
                data: seriesArray
            }]
        });
    }
});



$("a[href='#candig_patients']").on('shown.bs.tab', function(e) {
    window.history.pushState("", "Patients Overview", "#candig_patients");

    var patientStatusCode = 0;
    activeTab = e.target;
    patient_main();

    function replace_undefined(targetList) {
        for (let i = 0; i < targetList.length; i++){
            if (targetList[i] == "undefined" || targetList[i] == undefined) {
                targetList[i] = "N/A"
            }
        }

        return targetList
    }

    function patient_main() {
        if (document.getElementById('mytable').innerHTML != "") {
            var table = $("#mytable").DataTable();
            table.destroy();
            document.getElementById("mytable").innerHTML = "";
        }

        if (document.getElementById('patientTable').innerHTML != "") {
            var table = $("#patientTable").DataTable();
            table.destroy();
            document.getElementById("patientTable").innerHTML = "";
        }


        var listOfRace = [];
        var listOfProvinces = [];
        var listOfGenders = [];

        makeRequest("patients/search", {"datasetId": datasetId}).then(function(response) {
            var data = JSON.parse(response);

            var patientsDataset = data['results']['patients'];

            var tbl = $('<table/>').attr("id", "mytable");

            var th = '<thead><tr><th scope="col">Patient ID</th><th scope="col">Gender</th><th scope="col">Date of Death</th><th scope="col">Province of Residence</th> <th scope="col">Date of Birth</th><th scope="col">Race</th><th scope="col">Occupational Or Environmental Exposure</th></tr></thead><tbody>';

            $("#mytable").append(th);

            for (var i = 0; i < patientsDataset.length; i++) {

                listOfRace.push(patientsDataset[i]["race"]);
                listOfProvinces.push(patientsDataset[i]["provinceOfResidence"]);
                listOfGenders.push(patientsDataset[i]["gender"]);

                var tr = "<tr>";
                var td0 = '<td scope="col">' + patientsDataset[i]["patientId"] + "</td>";
                var tdGender = '<td scope="col">' + patientsDataset[i]["gender"] + "</td>";
                var td1 = '<td scope="col">' + patientsDataset[i]["dateOfDeath"] + "</td>";
                var td2 = '<td scope="col">' + patientsDataset[i]["provinceOfResidence"] + "</td>";
                var td3 = '<td scope="col">' + patientsDataset[i]["dateOfBirth"] + "</td>";
                var td4 = '<td scope="col">' + patientsDataset[i]["race"] + "</td>";
                var td5 = '<td scope="col">' + patientsDataset[i]["occupationalOrEnvironmentalExposure"] + "</td>";
                var td6 = "</tr>";

                var tempRow = tr + td0 + tdGender + td1 + td2 + td3 + td4 + td5 + td6
                var updatedRow = tempRow.replace(/undefined/g, "N/A")

                $("#mytable").append(updatedRow);
            }

            listOfRace = replace_undefined(listOfRace)
            listOfProvinces = replace_undefined(listOfProvinces)
            listOfGenders = replace_undefined(listOfGenders)

            categoriesDrawer("raceGraph", "Ethnic Groups", listOfRace);
            categoriesDrawer("provinceGraph", "Provinces", listOfProvinces);
            categoriesDrawer("genderGraph", "Genders", listOfGenders);

            $("#mytable").append('</tbody><tfoot><tr><th scope="col">Patient ID</th><th scope="col">Gender</th><th scope="col">Date of Death</th><th scope="col">Province of Residence</th> <th scope="col">Date of Birth</th><th scope="col">Race</th><th scope="col">OEE</th></tr></tfoot>');

            $(document).ready(function() {
                $('#mytable').DataTable({
                    initComplete: function() {
                        this.api().columns().every(function() {
                            var column = this;
                            var select = $('<select><option value=""></option></select>')
                                .appendTo($(column.footer()).empty())
                                .on('change', function() {
                                    var val = $.fn.dataTable.util.escapeRegex(
                                        $(this).val()
                                    );

                                    column
                                        .search(val ? '^' + val + '$' : '', true, false)
                                        .draw();
                                });

                            column.data().unique().sort().each(function(d, j) {
                                select.append('<option value="' + d + '">' + d + '</option>')
                            });
                        });
                    }
                });
            });

            $('#mytable tbody').on('click', 'tr', function() {
                var table = $("#mytable").DataTable();
                var tempData = table.row(this).data()[0];

                if (tempData != "N/A") {
                    patientInfoFetcher(tempData)
                }
                else {
                    alertBuilder("We are sorry, but the record you are trying to query doesn't have a valid id.");
                };
            });
        })
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

    function categoriesDrawer(elementId, titleText, arrayToDraw) {
        var tempCats = Object.keys(categoriesCounter(arrayToDraw));
        var tempVals = Object.values(categoriesCounter(arrayToDraw));
        var tempObjList = highChartSeriesObjectMaker(tempCats, tempVals);
        drillDownDrawer(elementId, titleText, tempCats, "", tempObjList, []);
    }

    function categoriesCounter(arrayToCount) {
        var result = {};
        for (var j = 0; j < arrayToCount.length; j++) {
            if (!result[arrayToCount[j]]) {
                result[arrayToCount[j]] = 0;
            }
            result[arrayToCount[j]]++;
        }
        return result;
    }

    function drillDownDrawer(elementId, titleText, categories, seriesName, seriesList, drillDownList) {
        var lastSearch = "";
        Highcharts.chart(elementId, {
            chart: {
                type: 'pie'
            },
            title: {
                text: titleText
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: categories
            },

            legend: {
                enabled: false
            },

            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    depth: 35,
                    dataLabels: {
                        enabled: true
                    },
                    point: {
                        events: {
                            click: function() {
                                if (lastSearch != this.name) {
                                    $('#mytable').DataTable().search(this.name).draw();
                                    lastSearch = this.name;
                                } else if (lastSearch == this.name) {
                                    $('#mytable').DataTable().search("").draw();
                                    lastSearch = "";
                                }
                            }
                        }
                    }
                }
            },

            series: [{
                // type: 'pie',
                name: seriesName,
                colorByPoint: true,
                data: seriesList
            }],
            drilldown: {
                series: drillDownList
            }
        });
    }

    function patientInfoFetcher(patientId) {

        if (patientStatusCode == 1) {
            var table = $("#patientTable").DataTable();
            try {
                table.destroy();
            }
            catch(err) {
                //pass
            }
            document.getElementById("patientTable").innerHTML = "";
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", prepend_path + "/samples/search", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
        xhr.send(JSON.stringify({
            'datasetId': datasetId,
            'filters': [{
                "field": "patientId",
                "operator": "==",
                "value": patientId

        }]}));
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);
            var sampleDataset = data['results']['samples'];

            xhr.open("POST", prepend_path + "treatments/search", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
            xhr.send(JSON.stringify({
                'datasetId': datasetId,
                'filters': [{
                    "field": "patientId",
                    "operator": "==",
                    "value": patientId

            }]}));
            xhr.onload = function() {
                var tempRes = JSON.parse(this.responseText);
                var treatmentDataset = tempRes['results']['treatments'];

                var tbl = $('<table/>').attr("id", "patientTable");
                var th = '<thead><tr><th scope="col">Patient ID</th><th scope="col">Collection Hospital</th><th scope="col">Collection Date</th><th scope="col">Cancer Type</th><th scope="col">Response to treatment</th><th scope="col">Drug list</th><th scope="col">Therapeutic Modality </th></tr></thead><tbody>';

                $("#patientTable").append(th);

                for (var i = 0; i < sampleDataset.length; i++) {

                    var tr = "<tr>";
                    var td0 = '<td scope="col">' + sampleDataset[i]["patientId"] + "</td>";
                    var td1 = '<td scope="col">' + sampleDataset[i]["collectionHospital"] + "</td>";
                    var td2 = '<td scope="col">' + sampleDataset[i]["collectionDate"] + "</td>";
                    var td7 = '<td scope="col">' + sampleDataset[i]["cancerType"] + "</td>";

                    var td3 = '<td scope="col">' + treatmentDataset[i]["responseToTreatment"] + "</td>";
                    var td4 = '<td scope="col">' + treatmentDataset[i]["drugListOrAgent"] + "</td>";
                    var td5 = '<td scope="col">' + treatmentDataset[i]["therapeuticModality"] + "</td>";
                    var td6 = "</tr>";

                    var tempRow = tr + td0 + td1 + td2 + td7 + td3 + td4 + td5 + td6
                    var updatedRow = tempRow.replace(/undefined/g, "N/A")

                    $("#patientTable").append(updatedRow);
                }

                $("#patientTable").append('</tbody>')

                $(document).ready(function() {
                    $("#patientTable").DataTable();
                    patientStatusCode = 1;
                });
            }
        }

    }
});

var statusCode = 0; // Initial value, table is empty

function submit() {
    $("#firstRG").empty();
    $("#secondRG").empty();
    $("#igvSample").empty();

    if (statusCode == 1) {
        if (document.getElementById('myTable').innerHTML != "") {
            var table = $('#myTable').DataTable();
            table.destroy();
            document.getElementById('myTable').innerHTML = "";
        }
    }

    document.getElementById("loader").style.display = "block";
    document.getElementById("myTable").innerHTML = "";

    document.getElementById("readGroupSelector").style.display = "none"
    var geneRequest = document.getElementById("request").value;

    var geneRequestObj = {
        'datasetId': datasetId,
        'gene': geneRequest
    }

    makeRequest("/variantsbygenesearch", geneRequestObj).then(function(response) {
        var data = JSON.parse(response)
        var geneDataset = data['results']['variants'];
        tableMaker(geneDataset);
        readGroupFetcher(geneRequest, geneDataset)
        document.getElementById("igvSample").style.display = "block";
            statusCode = 1; // The Dataset was created successfully
    }, function(Error) {
            document.getElementById("loader").style.display = "none";
            document.getElementById("igvSample").style.display = "none";
            document.getElementById("myTable").innerHTML = "Sorry, but we are not able to locate the gene.";
            statusCode = -1; //The dataset failed to initialized.
    })
}

function freqCounter(arrayToCount) {
    result = {};

    for (var j = 0; j < arrayToCount.length; j++) {
        if (!result[arrayToCount[j]]) {
            result[arrayToCount[j]] = 0;
        }
        ++result[arrayToCount[j]];
    }

    return result;
}

let readGroupDict = {}

function readGroupFetcher(geneRequest, geneDataset) {
    makeRequest("readgroupsets/search", {"datasetId": datasetId}).then(function(response) {
        var data = JSON.parse(response);
        var readGroupIds = [];
        var referenceSetIds = [];

        try {
            let finalChrId;
            let tempBody = data['results']["readGroupSets"]; //an array of readgroupsets
            let readGroupSetId = [];
            let readGroupSetName = []


            for (let i = 0; i < tempBody.length; i++) {
                readGroupSetId.push(tempBody[i]["id"]);
                readGroupIds.push(tempBody[i]["readGroups"][0]["id"]);
                referenceSetIds.push(tempBody[i]["readGroups"][0]["referenceSetId"])
                readGroupSetName.push(tempBody[i]["name"])
            }

            for (var j = 0; j < 1; j++) {
                let tempCurrData = geneDataset[j];
                let tempChrId = tempCurrData['referenceName'];

                if (tempChrId.includes('chr')) {
                    finalChrId = tempChrId.replace("chr", "");
                } else if (parseInt(tempChrId) != NaN) {
                    finalChrId = tempChrId;
                }

                else {
                    alertBuilder("We are sorry, but some parts of IGV may not work correctly.")
                }

            }

            readGroupDict["geneRequest"] = geneRequest
            readGroupDict["referenceSetIds"] = referenceSetIds[0]
            readGroupDict["chromesomeId"] = finalChrId
            readGroupDict["readGroupIds"] = readGroupIds
            readGroupDict["readGroupSetId"] = readGroupSetId
            readGroupDict["readGroupName"] = readGroupSetName

            let selectRG1 = document.getElementById("firstRG");
            let selectRG2 = document.getElementById("secondRG");

            for (let i = 0; i < readGroupSetId.length; i++){
                selectRG1.options[selectRG1.options.length] = new Option(readGroupSetName[i], readGroupSetId[i])
                selectRG2.options[selectRG2.options.length] = new Option(readGroupSetName[i], readGroupSetId[i])
            }

            document.getElementById("readGroupSelector").style.display = "block"

        } catch (err) {
            alertBuilder("We are sorry, but the IGV browser cannot be rendered.");
        }
    }, function(Error) {
        alertBuilder("We are sorry, but the IGV browser cannot be rendered.");
    })
}

function rg_submit() {

    var secondRgObj;

    try {
        let firstRG = document.getElementById("firstRG").value
        let secondRG = document.getElementById("secondRG").value

        if (firstRG == secondRG) {
            secondRgObj = ""
        }

        else secondRgObj = {
            sourceType: "ga4gh",
            type: "alignment",
            url: prepend_path + "",
            referenceId: "",
            readGroupIds: "",
            readGroupSetIds: "",
            name: ""
        }

        let firstRgReadGroupId = readGroupDict["readGroupIds"][readGroupDict["readGroupSetId"].indexOf(firstRG)]
        let firstRgReadGroupName = readGroupDict["readGroupName"][readGroupDict["readGroupSetId"].indexOf(firstRG)]

        let secondRgReadGroupId = readGroupDict["readGroupIds"][readGroupDict["readGroupSetId"].indexOf(secondRG)]
        let secondRgReadGroupName = readGroupDict["readGroupName"][readGroupDict["readGroupSetId"].indexOf(secondRG)]

        let firstRgObj = {"readGroupSetId": firstRG, "readGroupIds": firstRgReadGroupId, "name": firstRgReadGroupName}

        if (secondRgObj != ""){
            secondRgObj["readGroupIds"] = secondRgReadGroupId
            secondRgObj["readGroupSetIds"] = secondRG
            secondRgObj["name"] = secondRgReadGroupName
        }

        referenceIdFetcher(readGroupDict["geneRequest"], readGroupDict["referenceSetIds"], firstRgObj, secondRgObj, readGroupDict["chromesomeId"])
    }

    catch (err) {
        console.log("we are having problems fetching info")
    }

}

function referenceIdFetcher(geneRequest, referenceSetIds, firstRgObj, secondRgObj, chromesomeId) {
    makeRequest("references/search", {'referenceSetId': referenceSetIds,}).then(function(response) {

        let data = JSON.parse(response);
        let referenceId = "";

        try {
            let referencesList = data['results']["references"];

            for (let i = 0; i < referencesList.length; i++) {
                if (referencesList[i]["name"] == chromesomeId) {
                    referenceId = referencesList[i]["id"];
                }
            }

            if (secondRgObj != "") {
                secondRgObj["referenceId"] = referenceId
            }

            variantSetIdFetcher(geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId);
        } catch (err) {
            alertBuilder("We are sorry, but some parts of IGV may not work correctly.");
        }
    }, function(Error) {
        alertBuilder("We are sorry, but some parts of IGV may not work correctly.");
    })
}

function variantSetIdFetcher(geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId) {
    makeRequest("variantsets/search", {'datasetId': datasetId}).then(function(response) {
        let data = JSON.parse(response);
        let variantsetId;
        if (data['results']["variantSets"][0]["id"] != undefined) {
            variantsetId = data['results']["variantSets"][0]["id"];

            igvSearch(variantsetId, geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId);
        }
    })
}


function igvSearch(variantsetId, geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId) {
    var div = document.getElementById('igvSample')

    var options = {
        locus: geneRequest,
        genome: "hg19",
        reference: {
            id: "hg19",
            fastaURL: "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/1kg_v37/human_g1k_v37_decoy.fasta",
            cytobandURL: "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/b37/b37_cytoband.txt"
        },
        oauthToken: session_id,
        showRuler: true,
        tracks: [{
                sourceType: "ga4gh",
                type: "variant",
                url: prepend_path + "",
                referenceName: chromesomeId,
                variantSetId: variantsetId,
                name: "Variants",
                pageSize: 10000,
                visibilityWindow: 100000
            },
            {
                sourceType: "ga4gh",
                type: "alignment",
                url: prepend_path + "",
                referenceId: referenceId,
                readGroupIds: firstRgObj["readGroupIds"],
                readGroupSetIds: firstRgObj["readGroupSetId"],
                name: firstRgObj["name"]
            },
            secondRgObj,
            {
                name: "Genes",
                type: "annotation",
                format: "bed",
                sourceType: "file",
                url: "https://s3.amazonaws.com/igv.broadinstitute.org/annotations/hg19/genes/refGene.hg19.bed.gz",
                indexURL: "https://s3.amazonaws.com/igv.broadinstitute.org/annotations/hg19/genes/refGene.hg19.bed.gz.tbi",
                order: Number.MAX_VALUE,
                visibilityWindow: 300000000,
                displayMode: "EXPANDED",
                height: 300
            }

        ]
    };

    if (secondRgObj == "") {
        options["tracks"].splice(2, 1)
    }

    let browser = igv.createBrowser(div, options);
}


function tableMaker(geneDataset) {
    var clickableName;
    var tbl = $('<table/>').attr("id", "myTable");
    //$("#myTable").append(tbl);
    var tempRefName;
    var fullRefName;
    var result = {};

    var th = '<thead><tr><th scope="col" >Reference Name</th><th scope="col">Start</th><th scope="col">End</th> <th scope="col">Length</th><th scope="col">Reference Bases</th><th scope="col">Alternate Bases</th><th scope="col">Frequency</th><th scope="col">Names</th></tr></thead><tbody>';
    $("#myTable").append(th);

    var simplifiedObjArray = []

    for (var j = 0; j < geneDataset.length; j++) {
        var tempCurrData = geneDataset[j];

        var tempObj = {
            'referenceName': tempCurrData['referenceName'],
            'start': tempCurrData['start'],
            'end': tempCurrData['end'],
            'referenceBases': tempCurrData['referenceBases'],
            'alternateBases': tempCurrData['alternateBases'],
            'names': tempCurrData['names']
        }
        simplifiedObjArray.push(JSON.stringify(tempObj));
    }

    for (var j = 0; j < simplifiedObjArray.length; j++) {
        if (!result[simplifiedObjArray[j]]) {
            result[simplifiedObjArray[j]] = 0;
        }
        ++result[simplifiedObjArray[j]];
    }

    var processedDataset = Object.keys(result);
    var frequencyDataset = Object.values(result);

    for (var i = 0; i < processedDataset.length; i++) {
        var currDataset = JSON.parse(processedDataset[i]);
        var tr = "<tr>";

        var tempRefName = currDataset["referenceName"];
        if (tempRefName.includes('chr')) {
            fullRefName = tempRefName.replace("chr", "Chromosome ");
        } else fullRefName = "Chromosome " + tempRefName;

        var td0 = '<td scope="col">' + fullRefName + "</td>";
        var td1 = '<td scope="col">' + currDataset["start"] + "</td>";
        var length = currDataset["end"] - currDataset["start"];
        var tdLength = '<td scope="col">' + length + "</td>";
        var td2 = '<td scope="col">' + currDataset["end"] + "</td>";
        var td3 = '<td scope="col">' + currDataset["referenceBases"] + "</td>";
        var td4 = '<td scope="col">' + currDataset["alternateBases"] + "</td>";
        var tdFreq = '<td scope="col">' + frequencyDataset[i].toString() + "</td>";

        if (currDataset["names"] != undefined) {
            clickableName = "";
            for (var j = 0; j < currDataset["names"].length; j++) {
                if (currDataset["names"][j].includes('rs')) {
                    if (j > 0) {
                        clickableName += ", "
                    };
                    clickableName += '<a href="' + 'https://www.ncbi.nlm.nih.gov/SNP/snp_ref.cgi?rs=' + currDataset["names"][j] + '">' + currDataset["names"][j] + '</a>';
                } else if (currDataset["names"][j].includes('COSM')) {
                    if (j > 0) {
                        clickableName += ", "
                    };
                    clickableName += '<a href="' + 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + currDataset["names"][j].split('COSM')[1] + '">' + currDataset["names"][j] + '</a>';
                } else {
                    if (j > 0) {
                        clickableName += ", "
                    };
                    clickableName += ", " + currDataset["names"][j];
                }
            }
        } else clickableName = 'Not Found';

        var td5 = '<td scope="col">' + clickableName + "</td>";
        var td6 = "</tr>";

        $("#myTable").append(tr + td0 + td1 + td2 + tdLength + td3 + td4 + tdFreq + td5 + td6);
    }
    $("#myTable").append('</tbody>');

    $(document).ready(function() {
        $('#myTable').DataTable();
        document.getElementById("myTable_info").innerHTML += ", aggregated from " + geneDataset.length + " records.";
    });

    document.getElementById("title").style.marginTop = "50px";
    document.getElementById("loader").style.display = "none";
}

function logout() {
    makeRequest("/logout_oidc", {}).then(function(response){
        window.location.href = logout_url;
    })
}

$('.alert').on('close.bs.alert', function (e) {
    // prevent the alert from being removed from DOM
    e.preventDefault();
    var warningMsg = document.getElementById('warningMsg');
    warningMsg.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>'
    warningMsg.style.display = "none";
});

function alertBuilder(message) {
    let warningMsg = document.getElementById('warningMsg');
    warningMsg.style.display = "block";
    warningMsg.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>'
    warningMsg.innerHTML += message;
}