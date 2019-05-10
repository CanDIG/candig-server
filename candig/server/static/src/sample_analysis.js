"use strict";

let sample_analysis_instance;

$(window).on('load', function() {

    makeRequest("datasets/search", {}).then(function (response) {

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

        sample_analysis_instance = new sample_analysis();
        sample_analysis_instance.initialize();
        
    }, function (Error) {
        alertBuilder("No data currently available. Please contact a system administrator for assistance.")
    })
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    document.getElementById("warningMsg").style.display = "none";
    setCookie("datasetId", datasetId);
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
    sample_analysis_instance.initialize();
}

var tableIds = ["extractions", "alignments", "sequencing", "variantcalling", "fusiondetection", "expressionanalysis"];


function sample_analysis() {
    document.getElementById("sampleSearch").addEventListener("click", caller);

    this.initialize = function() {
        document.getElementById("sample_analysis_title").style.marginTop = "10%";
        document.getElementById("sample_analysis_title").style.marginBottom = "100px";
        document.getElementById("extractions").innerHTML = "";
        document.getElementById("alignments").innerHTML = "";
        document.getElementById("sequencing").innerHTML = "";
        document.getElementById("variantcalling").innerHTML = "";
        document.getElementById("fusiondetection").innerHTML = "";
        document.getElementById("expressionanalysis").innerHTML = "";
        document.getElementById("sampleSelect").innerHTML = "";
        sampleIDsFetcher();
    }

    function caller() {

        document.getElementById("sample_analysis_title").style.marginTop = "50px";
        document.getElementById("sample_analysis_title").style.marginBottom = "50px";

        var request = document.getElementById("sampleSelect").value;

        for (let i = 0; i < tableIds.length; i++) {
            xhrInitiator(tableIds[i], tableIds[i], request)
        }
    }

    // Initiates XHR calls to different endpoints
    function xhrInitiator(endpoint, element, request) {
        let requestObj = {
            'datasetId': datasetId,
            "filters": [{
                "field": "sampleId",
                "operator": "==",
                "value": request
            }]
        }

        makeRequest(endpoint + "/search", requestObj).then(function (response) {
            tableBuilder(JSON.parse(response), endpoint, element);
        }, function (Error) {
            alertBuilder("One or more tables are not available at this time.")
        })
    }

    function sampleIDsFetcher() {
        makeRequest("samples/search", {
            "datasetId": datasetId
        }).then(function (response) {
            var data = JSON.parse(response)["results"]["samples"];
            let sampleSelect = document.getElementById("sampleSelect");
            let listOfSampleIds = [];

            for (let i = 0; i < data.length; i++) {
                if (data[i]["sampleId"] != undefined) {
                    listOfSampleIds.push(data[i]["sampleId"]);
                }
            }

            selectPopulator("sampleSelect", listOfSampleIds.sort());

        }, function (Error) {
            alertBuilder("No data currently available, either the server does not have it, or you do not have access to them.")
        })
    }

    function selectPopulator(id, array) {
        let selectId = document.getElementById(id);

        for (let i = 0; i < array.length; i++) {
            selectId.options[selectId.options.length] = new Option(array[i], array[i])
        }
    }

    function tableBuilder(results, endpoint, id) {
        document.getElementById(id).innerHTML = "";
        var dataset = results["results"][endpoint];
        var keyList = Object.keys(dataset[0]);
        var columnDefs = [];
        var newHeader;
        var hiddenHeaders = ["id", "datasetId", "name"];

        for (var i = 0; i < keyList.length; i++) {
            newHeader = {}

            if (!hiddenHeaders.includes(keyList[i])) {
                columnDefs.push(keyList[i]);
            }
        }

        var newColumnDefs = [{
            "headerName": endpoint,
            "field": "field"
        }, {
            "headerName": "",
            "field": "value"
        }];

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

    function gridMaker(newColumnDefs, newDataset, id) {

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
}