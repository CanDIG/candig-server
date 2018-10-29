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

        if (getCookie("datasetId") == null) {
            datasetId = finalDatasetId[0];
            $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[0]);
        }

        else {
            datasetId = getCookie("datasetId")
            $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
        }

    }, function(Error) {
        alertBuilder("No data currently available. Please contact a system administrator for assistance.")
    })
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    document.getElementById("warningMsg").style.display = "none";
    setCookie("datasetId", datasetId);
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
}


var statusCode = 0; // Initial value, table is empty

    $("#firstRG").empty();
    $("#secondRG").empty();
    $("#igvSample").empty();
    document.getElementById("request").value = "";
    document.getElementById("readGroupSelector").style.display = "none";
    document.getElementById("geneTable_wrap").style.display = "none";
    document.getElementById("title").style.marginTop = "10%";

    // If the dataTable is not initialized, statusCode == -1 meaning that the previous response was invalid
    if (document.getElementById('geneTable').innerHTML != "" && statusCode != -1) {
        var table = $("#geneTable").DataTable();
        table.destroy();
        document.getElementById("geneTable").innerHTML = "";
        statusCode = 0;
    }

    document.getElementById("searchBtn").addEventListener("click", submit);
    document.getElementById("confirmRG").addEventListener("click", rg_submit);

    function submit() {
        $("#firstRG").empty();
        $("#secondRG").empty();
        $("#igvSample").empty();

        if (statusCode == 1) {
            if (document.getElementById('geneTable').innerHTML != "") {
                var table = $('#geneTable').DataTable();
                table.destroy();
                document.getElementById('geneTable').innerHTML = "";
            }
        }

        document.getElementById("loader").style.display = "block";
        document.getElementById("geneTable").innerHTML = "";

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
                document.getElementById("geneTable").innerHTML = "Sorry, but we are not able to locate the gene.";
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
        var tbl = $('<table/>').attr("id", "geneTable");
        //$("#geneTable").append(tbl);
        var tempRefName;
        var fullRefName;
        var result = {};

        var th = '<thead><tr><th scope="col" >Reference Name</th><th scope="col">Start</th><th scope="col">End</th> <th scope="col">Length</th><th scope="col">Reference Bases</th><th scope="col">Alternate Bases</th><th scope="col">Frequency</th><th scope="col">Names</th></tr></thead><tbody>';
        $("#geneTable").append(th);

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

            $("#geneTable").append(tr + td0 + td1 + td2 + tdLength + td3 + td4 + tdFreq + td5 + td6);
        }
        $("#geneTable").append('</tbody>');

        $(document).ready(function() {
            $('#geneTable').DataTable();
            document.getElementById("geneTable_info").innerHTML += ", aggregated from " + geneDataset.length + " records.";
        });

        document.getElementById("geneTable_wrap").style.display = "block";
        document.getElementById("title").style.marginTop = "50px";
        document.getElementById("loader").style.display = "none";
    }
