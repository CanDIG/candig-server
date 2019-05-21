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

    }, function(Error) {
        alertBuilder("No datasets currently available. Please contact a system administrator for assistance.");
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
            'gene': geneRequest,
            'pageSize': '10000'
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
                alertBuilder("Sorry, but no data is available for the gene you searched.")
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

    let readGroupsetsDict = {}

    /**
     * Request a list of readGroupsets, and populate the select fields.
     * @param {string} geneRequest: The responses returned by all promises.
     * @param {string} geneDataset: The response returned for the previous user input.
    */
    function readGroupFetcher(geneRequest, geneDataset) {
        makeRequest("readgroupsets/search", {"datasetId": datasetId}).then(function(response) {
            var listOfReadGroupSets = JSON.parse(response)['results']["readGroupSets"];
            let listOfReadGroupSetsNames = []
            readGroupsetsDict = {}

            try {
                // It takes the first element of geneDataset because the variants of the same gene are assumed to be positioned in the same chromosome
                let chromesomeId = geneDataset[0]['referenceName'].replace('chr', '')

                for (let i = 0; i < listOfReadGroupSets.length; i++) {
                    let readGroupIds = []

                    let temp_rg_igv = {
                        referenceId: "",
                        referenceSetId: listOfReadGroupSets[i]["readGroups"][0]["referenceSetId"],
                        readGroupSetIds: listOfReadGroupSets[i]["id"],
                        name: listOfReadGroupSets[i]["name"]
                    }

                    // Iterate through readGroups to find all readGroupIds
                    for (let j = 0; j < listOfReadGroupSets[i]["readGroups"].length; j++) {
                        readGroupIds.push(listOfReadGroupSets[i]["readGroups"][j]["id"]);
                    }

                    temp_rg_igv["readGroupIds"] = readGroupIds;

                    readGroupsetsDict[listOfReadGroupSets[i]["name"]] = temp_rg_igv;
                }

                readGroupsetsDict["chromesomeId"] = chromesomeId;
                readGroupsetsDict["geneRequest"] = geneRequest;

                let rgSelect = document.getElementById("rgSelect");
                rgSelect.innerHTML = "";

                // Sort the list of readGroupSets
                for (let i = 0; i < listOfReadGroupSets.length; i++){
                    listOfReadGroupSetsNames.push(listOfReadGroupSets[i]['name']);
                }

                listOfReadGroupSetsNames.sort();

                for (let i = 0; i < listOfReadGroupSetsNames.length; i++) {
                    rgSelect.options[rgSelect.options.length] = new Option(listOfReadGroupSetsNames[i], listOfReadGroupSetsNames[i])
                }

                $('.selectpicker').selectpicker('refresh');

                document.getElementById("readGroupSelector").style.display = "block"

            } catch (err) {
                alertBuilder("We are sorry, but the IGV browser cannot be rendered.");
            }
        }, function(Error) {
            alertBuilder("We are sorry, but the IGV browser cannot be rendered.");
        })
    }


    /**
     * Generate multiple promises to contruct IGV alignment and variants objects on user submission.
    */

    function rg_submit() {

        let selectedValues = $('.selectpicker').val();

        alertCloser();

        if (selectedValues == null || selectedValues.length > 3) {
            alertBuilder("Please specify at least one, but no more than three read group sets.");
        }

        else {
            try {

                let promises = [];

                // One promise is needed for every reference ID search.
                for (let i = 0; i < selectedValues.length; i++) {
                    let newPromise = referenceIdFetcher(readGroupsetsDict[selectedValues[i]]['referenceSetId'], selectedValues[i], readGroupsetsDict['chromesomeId']);
                    promises.push(newPromise);
                }

                // Only one promise is needed for all variant sets.
                promises.push(variantSetIdFetcher(selectedValues));

                Promise.all(promises).then(function(values){
                    igvCaller(values, readGroupsetsDict['chromesomeId'], selectedValues, readGroupsetsDict['geneRequest']);
                })
            }
            catch (err) {
                alertBuilder("The IGV Browser cannot be rendered for the selected read group sets.")
            }            
        }
    }

    /**
     * Construct the tracks object that includes both alignments and variants.
     * @param {string} values: The responses returned by all promises.
     * @param {string} chromesomeId: The responses returned by all 3 promises.
     * @param {array} selectedValues: The list of readGroupSets selected by the user.
     * @param {string} geneRequest: The gene searched by the user.
    */

    function igvCaller(values, chromesomeId, selectedValues, geneRequest) {

        let track = [];
        let trackOfVariants;
        let trackOfAlignments;

        for (let i = 0; i < values.length; i++) {
            // case 1: referenceId
            if (values[i]['referenceId']) {
                readGroupsetsDict[values[i]['name']]['referenceId'] = values[i]['referenceId'];
            }
            // case 2: variantSetId
            else {
                trackOfVariants = variantsTrackGenerator(values[i], chromesomeId);
            }
        }

        trackOfAlignments = alignmentTrackGenerator(selectedValues);

        let tracks = track.concat(trackOfVariants, trackOfAlignments);

        tracks.push({
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
        })

        igvSearch(geneRequest, tracks);
    }

    /**
     * Generate alignment track objects used by IGV browser.
     * @param {array} listOfAlignments: A list of alignments' names.
     * @return a Promise with the constructed IGV alignment object
    */
    function alignmentTrackGenerator(listOfAlignments) {

        let trackOfAlignments = [];

        for (let i = 0; i < listOfAlignments.length; i++) {
            let igv_alignment_object = {
                sourceType: "ga4gh",
                type: "alignment",
                url: prepend_path + "",
                referenceId: readGroupsetsDict[listOfAlignments[i]]['referenceId'],
                readGroupIds: readGroupsetsDict[listOfAlignments[i]]['readGroupIds'],
                readGroupSetIds: readGroupsetsDict[listOfAlignments[i]]['readGroupSetIds'],
                name: listOfAlignments[i]
            };

            if (trackOfAlignments.length == 0){
                trackOfAlignments.push(igv_alignment_object);
            }
            else if (trackOfAlignments[0]['name'] != igv_alignment_object['name']) {
                trackOfAlignments.push(igv_alignment_object);
            }
        }

        return trackOfAlignments;
    }

    /**
     * Request referenceId given the names of variantSets.
     * @param {array} listOfVariantSets: A list of variantsets' names.
     * @param {string} chromesomeId: The chromosomeId.
     * @return a Promise with the constructed IGV variants object
    */
    function variantsTrackGenerator(listOfVariantSets, chromesomeId) {
        let trackOfVariants = [];

        for (let j = 0; j < listOfVariantSets.length; j++) {

            let igv_variant_object = {
                sourceType: "ga4gh",
                type: "variant",
                url: prepend_path + "",
                referenceName: chromesomeId,
                variantSetIds: "",
                name: "",
                pageSize: 10000,
                visibilityWindow: 100000
            };

            igv_variant_object['name'] = listOfVariantSets[j]['name'];
            igv_variant_object['variantSetId'] = listOfVariantSets[j]['variantSetId'];

            trackOfVariants.push(igv_variant_object);
        }

        return trackOfVariants;
    }


    /**
     * Request referenceId given the names of variantSets.
     * @param {string} referenceSetId: The referenceSetId.
     * @param {string} readGroupSetName: The readGroupSetName.
     * @param {string} chromesomeId: The chromosomeId.
     * @return a Promise with readGroupSets' names being the keys, and their referenceId being the value.
    */
    function referenceIdFetcher(referenceSetId, readGroupSetName, chromesomeId) {
        return new Promise(function(resolve, reject) {
            makeRequest("references/search", {'referenceSetId': referenceSetId}).then(function(response) {

                let referenceId = "";

                try {
                    let referencesList = JSON.parse(response)['results']["references"];

                    for (let i = 0; i < referencesList.length; i++) {
                        let currReferenceId = referencesList[i]["name"].replace("chr", "");

                        if (currReferenceId == chromesomeId) {
                            referenceId = referencesList[i]["id"];
                        }
                    }

                    resolve({"name": readGroupSetName, "referenceId": referenceId})
                } catch (err) {
                    reject({"name": readGroupSetName, "referenceId": ""})
                    alertBuilder("We are sorry, but some parts of IGV may not work correctly.");
                }
            }, function(Error) {
                reject({"name": readGroupSetName, "referenceId": ""})
                alertBuilder("We are sorry, but some parts of IGV may not work correctly.");
            })
        })
    }

    /**
     * Request variantsetIds given the names of variantSets.
     * @param {array} listOfSelectedRG: List of selectedRG.
     * @return a Promise with readGroupSets' names being the keys, and their variantSetId being the value.
    */
    function variantSetIdFetcher(listOfSelectedRG) {
        return new Promise(function(resolve, reject) {
            makeRequest("variantsets/search", {'datasetId': datasetId}).then(function(response) {
                let listOfVariantSets = JSON.parse(response)['results']['variantSets'];
                let responseObjList = [];

                for (let i = 0; i < listOfVariantSets.length; i++) {
                    if (listOfSelectedRG.includes(listOfVariantSets[i]['name'])) {
                        let responseObj = {};
                        responseObj['name'] = listOfVariantSets[i]['name']
                        responseObj['variantSetId'] = listOfVariantSets[i]['id'];
                        responseObjList.push(responseObj)
                    }
                }
                resolve(responseObjList);
            })
        })
    }

    /**
     * Invoke a new IGV browser instance.
     * @param {string} geneRequest: The gene searched by the user.
     * @param {array} tracks: a list of IGV alignment and variant sobjects.
    */
    function igvSearch(geneRequest, tracks) {
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
            tracks: tracks
        };

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
