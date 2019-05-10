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
        patient_main();

    }, function(Error) {
        alertBuilder("No datasets currently available. Please contact a system administrator for assistance.");
        noPermissionMessageMultiple(['raceGraph', 'provinceGraph', 'genderGraph']);
    })
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    document.getElementById("warningMsg").style.display = "none";
    setCookie("datasetId", datasetId);
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
    patient_main();
}

var patientStatusCode = 0;

let loader = '<div class="loader_bar"></div>'
document.getElementById("raceGraph").innerHTML = loader;
document.getElementById("genderGraph").innerHTML = loader;
document.getElementById("provinceGraph").innerHTML = loader;

function replace_undefined(targetList) {
    for (let i = 0; i < targetList.length; i++) {
        if (targetList[i] == "undefined" || targetList[i] == undefined) {
            targetList[i] = "N/A"
        }
    }
    return targetList
}

function patient_main() {
    if (document.getElementById('patients_table').innerHTML != "") {
        try {
            var table = $("#patients_table").DataTable();
            table.destroy();
        } catch (err) {
            //pass
        }
        document.getElementById("patients_table").innerHTML = "";
    }

    if (document.getElementById('mergedTreatmentsDiagnosesTable').innerHTML != "") {
        try {
            var table = $("#mergedTreatmentsDiagnosesTable").DataTable();
            table.destroy();
        } catch (err) {
            //pass
        }
        document.getElementById("mergedTreatmentsDiagnosesTable").innerHTML = "";
    }

    var listOfRace = [];
    var listOfProvinces = [];
    var listOfGenders = [];

    makeRequest("patients/search", {
        "datasetId": datasetId
    }).then(function(response) {
        var data = JSON.parse(response);

        var patientsDataset = data['results']['patients'];

        var tbl = $('<table/>').attr("id", "patients_table");

        var th = '<thead><tr><th scope="col">Patient ID</th><th scope="col">Gender</th><th scope="col">Date of Death</th><th scope="col">Province of Residence</th> <th scope="col">Date of Birth</th><th scope="col">Race</th><th scope="col">Occupational Or Environmental Exposure</th></tr></thead><tbody>';

        $("#patients_table").append(th);

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

            $("#patients_table").append(updatedRow);
        }

        listOfRace = replace_undefined(listOfRace)
        listOfProvinces = replace_undefined(listOfProvinces)
        listOfGenders = replace_undefined(listOfGenders)

        categoriesDrawer("raceGraph", "Ethnic Groups", listOfRace);
        categoriesDrawer("provinceGraph", "Provinces", listOfProvinces);
        categoriesDrawer("genderGraph", "Genders", listOfGenders);

        $("#patients_table").append('</tbody><tfoot><tr><th scope="col">Patient ID</th><th scope="col">Gender</th><th scope="col">Date of Death</th><th scope="col">Province of Residence</th> <th scope="col">Date of Birth</th><th scope="col">Race</th><th scope="col">OEE</th></tr></tfoot>');

        $(document).ready(function() {
            try {
                $('#patients_table').DataTable({
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
                                        .search("^" + this.value, true, false, true)
                                        .draw();
                                });

                            column.data().unique().sort().each(function(d, j) {
                                select.append('<option value="' + d + '">' + d + '</option>')
                            });
                        });
                    }
                });
            } catch (err) {
                alertBuilder("The table wasn't correctly rendered. Please refresh the page.")
            }

        });

        $('#patients_table tbody').off('click').on('click', 'tr', function() {
            var table = $("#patients_table").DataTable();
            var tempData = table.row(this).data()[0];

            if (tempData != "N/A") {
                patientInfoFetcher(tempData)
            } else {
                alertBuilder("We are sorry, but the record you are trying to query doesn't have a valid id.");
            };
        });
    }, function(Error) {
            noPermissionMessageMultiple(['raceGraph', 'provinceGraph', 'genderGraph']);
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
            type: 'pie',
            style: {
                fontFamily: "Roboto"
            }
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
                                $('#patients_table').DataTable().search(this.name).draw();
                                lastSearch = this.name;
                            } else if (lastSearch == this.name) {
                                $('#patients_table').DataTable().search("").draw();
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
        try {
            var table = $("#mergedTreatmentsDiagnosesTable").DataTable();
            table.destroy();
        } catch (err) {
            //pass
        }
        document.getElementById("mergedTreatmentsDiagnosesTable").innerHTML = "";
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

        }]
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
            'filters': [{
                "field": "patientId",
                "operator": "==",
                "value": patientId

            }]
        }));
        xhr.onload = function() {
            var tempRes = JSON.parse(this.responseText);
            var treatmentDataset = tempRes['results']['treatments'];

            var tbl = $('<table/>').attr("id", "mergedTreatmentsDiagnosesTable");
            var th = '<thead><tr><th scope="col">Patient ID</th><th scope="col">Collection Hospital</th><th scope="col">Collection Date</th><th scope="col">Cancer Type</th><th scope="col">Response to treatment</th><th scope="col">Drug list</th><th scope="col">Therapeutic Modality </th></tr></thead><tbody>';

            $("#mergedTreatmentsDiagnosesTable").append(th);

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

                $("#mergedTreatmentsDiagnosesTable").append(updatedRow);
            }

            $("#mergedTreatmentsDiagnosesTable").append('</tbody>')

            $(document).ready(function() {
                $("#mergedTreatmentsDiagnosesTable").DataTable();
                patientStatusCode = 1;
            });
        }
    }

}