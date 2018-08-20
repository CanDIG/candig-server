"use strict";

/*Retrieve a list of datasets and initialize the page*/
$(window).load(function() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/datasets/search", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({}));
    xhr.onload = function() {

        if (xhr.status != 200) {
            let warningMsg = document.getElementById('warningMsg');
            warningMsg.style.display = "block";
            document.getElementById('tab-content').style.display = "none";
            warningMsg.innerHTML += "No data currently available. Please contact a system administrator for assistance.";
        } else {
            const data = JSON.parse(this.responseText);
            const listOfDatasetId = data['results']['datasets'];

            if (listOfDatasetId.length == 0) {
                $('warningMsg').html("Sorry, but it seems like no data is available at the moment..")
            } else {
                let finalDatasetName = [];
                let finalDatasetId = [];
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
                $('#dropdownMenuLink').html("Dataset: " + finalDatasetName[0]);

                $('.nav-tabs a[href="#candig"]').tab('show');
            }
        }
    }
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    let currTab = activeTab.href.split('#')[1];
    $('#topTabs a[href="#' + "refreshTab" + '"]').tab('show');
    $('#topTabs a[href="#' + currTab + '"]').tab('show');
    $('#dropdownMenuLink').html("Dataset: " + finalDatasetName[datasetIndex]);
}

$("a[href='#gene_search']").on('shown.bs.tab', function(e) {
    activeTab = e.target;

    // If the dataTable is not initialized, statusCode == -1 meaning that the previous response was invalid
    if (document.getElementById('myTable').innerHTML != "" && statusCode != -1) {
        var table = $("#myTable").DataTable();
        table.destroy();
        document.getElementById("myTable").innerHTML = "";
        statusCode = 0;
    }

})

/*
The following chunk of function gets executed on load, or once the candig tab is selected
*/

$("a[href='#candig']").on('shown.bs.tab', function(e) {

    activeTab = e.target;
    var treatments;
    var objectDrugList = [];
    var drugList = Array(18).join(".").split("."); //Initialize an emptry string array that has 18 empty strings.

    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/treatments/search", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({
        'datasetId': datasetId
    }));
    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        var knownPeers = data['status']['Known peers'];
        var queriedPeers = data['status']['Queried peers'];
        var success = data['status']['Successful communications'];
        var queryStatusSeriesArray = highChartSeriesObjectMaker(["Known Peers", "Queried Peers", "Successful Communications"], [knownPeers, queriedPeers, success]);
        singleLayerDrawer("queryStatus", 'bar', 'Server status', queryStatusSeriesArray);

        samplesFetcher();

        cancerTypeDruglistFetcher();
        treatments = data['results']['treatments'];
        treatmentsFetcher(treatments);

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
        var xhr = new XMLHttpRequest();
        xhr.open("POST", prepend_path + "/samples/search", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
        xhr.send(JSON.stringify({
            'datasetId': datasetId
        }));
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);

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

        }
    }

    // This function calculates the cumulative sum over the years
    function timelineDrawer(yearsCount, years, cumulativeData) {
        Highcharts.chart('timelineSamples', {
            chart: {
                type: 'area'
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

    function drillDownDrawer(elementId, titleText, seriesName, seriesList, drillDownList) {
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
                data: seriesList
            }],
            drilldown: {
                series: drillDownList,
                drillUpButton: {
                    position: {
                        x: 0,
                        y: -40
                    }
                }
            }
        });
    }

    function cancerTypeDruglistFetcher() {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", prepend_path + "/diagnoses/search", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
        xhr.send(JSON.stringify({
            'datasetId': datasetId
        }));
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);
            var diagnosesDatasets = data['results']['diagnoses'];
            var result = {};
            var seriesList = [];
            var seriesObj = {};
            var drillDownList = [];
            var drillDownObj = {};
            var tempCancerList = [];

            for (var i = 0; i < diagnosesDatasets.length; i++) {
                if (diagnosesDatasets[i]['cancerType'] != undefined) {
                    tempCancerList.push(diagnosesDatasets[i]['cancerType']);
                }
            }

            var tempCancerObj = freqCounter(tempCancerList);
            var cancerTypesList = Object.keys(tempCancerObj);
            var cancerTypeFreq = Object.values(tempCancerObj);

            for (var i = 0; i < diagnosesDatasets.length; i++) {
                var currCancer = diagnosesDatasets[i]['cancerType'];
                drugList[cancerTypesList.indexOf(currCancer)] += treatments[i]['drugListOrAgent'];
                //cancerTypeFreq[cancerTypesList.indexOf(currCancer)]++;
            }

            for (var i = 0; i < cancerTypesList.length; i++) {
                seriesObj = {};
                seriesObj['name'] = cancerTypesList[i];
                seriesObj['y'] = cancerTypeFreq[i];
                seriesObj['drilldown'] = cancerTypesList[i];
                seriesList.push(seriesObj);
            }

            for (var j = 0; j < drugList.length; j++) {
                drugList[j] = drugList[j].split(", ");

                result = {};
                for (var k = 0; k < drugList[j].length; k++) {
                    if (!result[drugList[j][k]])
                        result[drugList[j][k]] = 0;
                    ++result[drugList[j][k]];
                }
                objectDrugList.push(result);
            }

            for (var i = 0; i < objectDrugList.length; i++) {
                drillDownObj = {};
                var tempData = Object.keys(objectDrugList[i]).map(function(key) {
                    return [String(key), objectDrugList[i][key]];
                });

                drillDownObj['id'] = cancerTypesList[i];
                drillDownObj['data'] = tempData;
                drillDownList.push(drillDownObj);
            }

            drillDownDrawer('cancerTypes', "cancer types and corresponding treatment drugs", 'cancer types', seriesList, drillDownList);

        }
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
        //Highcharts.setOptions(theme);
    }
});



$("a[href='#candig_patients']").on('shown.bs.tab', function(e) {

    var patientStatusCode = 0;
    activeTab = e.target;
    patient_main();

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
        var xhr = new XMLHttpRequest();
        xhr.open("POST", prepend_path + "/patients/search", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
        xhr.send(JSON.stringify({
            'datasetId': datasetId
        }));
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);

            var patientsDataset = data['results']['patients'];

            var tbl = $('<table/>').attr("id", "mytable");

            var th = '<thead><tr><th scope="col">Patient ID</th><th scope="col">Gender</th><th scope="col">Date of Death</th><th scope="col">Province of Residence</th> <th scope="col">Date of Birth</th><th scope="col">Race</th><th scope="col">OEE</th></tr></thead><tbody>';

            $("#mytable").append(th);

            for (var i = 0; i < patientsDataset.length; i++) {

                if (patientsDataset[i]["race"] != undefined && patientsDataset[i]["provinceOfResidence"] != undefined && patientsDataset[i]["gender"] != undefined) {
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

                    $("#mytable").append(tr + td0 + tdGender + td1 + td2 + td3 + td4 + td5 + td6);
                }
            }

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
                patientInfoFetcher(tempData);
            });

        }

    }


    function highChartSeriesObjectMaker(nameArray, dataArray) {
        var tempObj = {};
        var seriesObjList = [];
        var tempDataArray = [];
        for (var i = 0; i < nameArray.length; i++) {
            tempObj = {};
            //tempDataArray = [];
            tempObj['name'] = nameArray[i];
            //tempDataArray.push(dataArray[i]);
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
            table.destroy();
            document.getElementById("patientTable").innerHTML = "";
        }

        var xhr = new XMLHttpRequest();

        xhr.open("POST", prepend_path + "/samples/search", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
        xhr.send(JSON.stringify({
            'datasetId': datasetId,
            'patientId': patientId
        }));
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);
            var sampleDataset = data['results']['samples'];

            xhr.open("POST", prepend_path + "treatments/search", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
            xhr.send(JSON.stringify({
                'datasetId': datasetId,
                'patientId': patientId
            }));
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

                    $("#patientTable").append(tr + td0 + td1 + td2 + td7 + td3 + td4 + td5 + td6);
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

    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/variantsbygenesearch", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({
        'datasetId': datasetId,
        'gene': geneRequest
    }));
    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        if (xhr.status == 200) {
            var geneDataset = data['results']['variants'];
            tableMaker(geneDataset);
            readGroupFetcher(geneRequest, geneDataset)
            //igvSearch(geneRequest);
            document.getElementById("igvSample").style.display = "block";
            statusCode = 1; // The Dataset was created successfully
        } else {
            document.getElementById("loader").style.display = "none";
            document.getElementById("igvSample").style.display = "none";
            document.getElementById("myTable").innerHTML = "Sorry, but we are not able to locate the gene.";
            statusCode = -1; //The dataset failed to initialized.
        }
    }
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
    console.log("inside readgroup request")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/readgroupsets/search", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({
        'datasetId': datasetId,
    }));
    xhr.onload = function() {
        console.log("data is now loading")
        var data = JSON.parse(this.responseText);
        var readGroupIds = [];
        var referenceSetIds = [];
        if (xhr.status == 200) {
            //console.log("xhr status okay")
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
                        let warningMsg = document.getElementById('warningMsg');
                        warningMsg.style.display = "block";
                        warningMsg.innerHTML += "We are sorry, but some parts of IGV may not work correctly.";
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
                let warningMsg = document.getElementById('warningMsg');
                warningMsg.style.display = "block";
                warningMsg.innerHTML += "We are sorry, but the IGV browser cannot be rendered.";
            }
        } else {
            let warningMsg = document.getElementById('warningMsg');
            warningMsg.style.display = "block";
            warningMsg.innerHTML += "We are sorry, but the IGV browser cannot be rendered.";
        }
    }
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

    console.log("inside reference id fetcher")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/references/search", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({
        'referenceSetId': referenceSetIds,
    }));
    xhr.onload = function() {
        let data = JSON.parse(this.responseText);
        let referenceId = "";

        if (xhr.status == 200) {
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
                let warningMsg = document.getElementById('warningMsg');
                warningMsg.style.display = "block";
                warningMsg.innerHTML += "We are sorry, but some parts of IGV may not work correctly.";
            }

        } else {
            // do nothing for now
        }
    }
}

function variantSetIdFetcher(geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/variantsets/search", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send(JSON.stringify({
        'datasetId': datasetId,
    }));
    xhr.onload = function() {
        let data = JSON.parse(this.responseText);
        let variantsetId;
        if (data['results']["variantSets"][0]["id"] != undefined) {
            variantsetId = data['results']["variantSets"][0]["id"];

            igvSearch(variantsetId, geneRequest, referenceSetIds, firstRgObj, secondRgObj, referenceId, chromesomeId);
        }
    }
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
    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/logout_oidc", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer '+ session_id);
    xhr.send(JSON.stringify({
        'access': access,
        'refresh': refresh
    }));
    xhr.onload = function() {
        window.location.href = JSON.parse(xhr.response).redirect;
    }        
}