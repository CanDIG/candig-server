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
        } else {
            datasetId = getCookie("datasetId")
            $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
        }
        currentDatasetName = splitString(finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
        initialize();

    }, function(Error) {
        document.getElementById('tab-content').style.display = "none";
        alertBuilder("No data currently available. Please contact a system administrator for assistance.")
    })
});

function refreshDataset(datasetIndex) {
    datasetId = finalDatasetId[datasetIndex];
    document.getElementById("warningMsg").style.display = "none";
    setCookie("datasetId", datasetId);
    $('#dropdownMenuLink').html('<i class="fas fa-database"></i> ' + finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
    currentDatasetName = splitString(finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]);
    reloadGraphs();
}


var selectPopulated = 0;

let currentDatasetName = finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))];

const categories = {
    "patients": ["patientId", "otherIds", "dateOfBirth", "gender", "ethnicity", "race", "provinceOfResidence", "dateOfDeath",
        "causeOfDeath", "autopsyTissueForResearch", "priorMalignancy", "dateOfPriorMalignancy", "familyHistoryAndRiskFactors",
        "familyHistoryOfPredispositionSyndrome", "detailsOfPredispositionSyndrome", "geneticCancerSyndrome",
        "otherGeneticConditionOrSignificantComorbidity", "occupationalOrEnvironmentalExposure"
    ],
    "enrollments": ["patientId", "enrollmentInstitution", "enrollmentApprovalDate", "crossEnrollment", "otherPersonalizedMedicineStudyName",
        "otherPersonalizedMedicineStudyId", "ageAtEnrollment", "eligibilityCategory", "statusAtEnrollment", "primaryOncologistName",
        "primaryOncologistContact", "referringPhysicianName", "referringPhysicianContact", "summaryOfIdRequest", "treatingCentreName", "treatingCentreProvince"
    ],
    "treatments": ["patientId", "courseNumber", "therapeuticModality", "systematicTherapyAgentName", "treatmentPlanType", "treatmentIntent",
        "startDate", "stopDate", "reasonForEndingTheTreatment", "protocolNumberOrCode", "surgeryDetails", "radiotherapyDetails", "chemotherapyDetails",
        "hematopoieticCellTransplant", "immunotherapyDetails", "responseToTreatment", "responseCriteriaUsed", "dateOfRecurrenceOrProgressionAfterThisTreatment",
        "unexpectedOrUnusualToxicityDuringTreatment", "drugListOrAgent", "drugIdNumbers"
    ],
    "samples": ["patientId", "sampleId", "diagnosisId", "localBiobankId", "collectionDate", "collectionHospital", "sampleType", "tissueDiseaseState",
        "anatomicSiteTheSampleObtainedFrom", "cancerType", "cancerSubtype", "pathologyReportId", "morphologicalCode", "topologicalCode",
        "shippingDate", "receivedDate", "qualityControlPerformed", "estimatedTumorContent", "quantity", "units", "associatedBiobank",
        "otherBiobank", "sopFollowed", "ifNotExplainAnyDeviation"
    ],
    "diagnoses": ["patientId", "diagnosisId", "diagnosisDate", "ageAtDiagnosis", "cancerType", "classification", "cancerSite", "histology",
        "methodOfDefinitiveDiagnosis", "sampleType", "sampleSite", "tumorGrade", "gradingSystemUsed", "sitesOfMetastases", "stagingSystem",
        "versionOrEditionOfTheStagingSystem", "specificTumorStageAtDiagnosis", "prognosticBiomarkers", "biomarkerQuantification",
        "additionalMolecularTesting", "additionalTestType", "laboratoryName", "laboratoryAddress", "siteOfMetastases",
        "stagingSystemVersion", "specificStage", "cancerSpecificBiomarkers", "additionalMolecularDiagnosticTestingPerformed", "additionalTest"
    ],
    "tumourboards": ["patientId", "dateOfMolecularTumorBoard", "typeOfSampleAnalyzed", "typeOfTumourSampleAnalyzed", "analysesDiscussed",
        "somaticSampleType", "normalExpressionComparator", "diseaseExpressionComparator",
        "hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer", "actionableTargetFound",
        "molecularTumorBoardRecommendation", "germlineDnaSampleId", "tumorDnaSampleId", "tumorRnaSampleId",
        "germlineSnvDiscussed", "somaticSnvDiscussed", "cnvsDiscussed", "structuralVariantDiscussed",
        "classificationOfVariants", "clinicalValidationProgress", "typeOfValidation", "agentOrDrugClass",
        "levelOfEvidenceForExpressionTargetAgentMatch", "didTreatmentPlanChangeBasedOnProfilingResult",
        "howTreatmentHasAlteredBasedOnProfiling", "reasonTreatmentPlanDidNotChangeBasedOnProfiling",
        "detailsOfTreatmentPlanImpact", "patientOrFamilyInformedOfGermlineVariant",
        "patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling", "summaryReport"
    ],
    "outcomes": ["patientId", "physicalExamId", "dateOfAssessment", "diseaseResponseOrStatus", "otherResponseClassification",
        "minimalResidualDiseaseAssessment", "methodOfResponseEvaluation", "responseCriteriaUsed", "summaryStage",
        "sitesOfAnyProgressionOrRecurrence", "vitalStatus", "height", "weight", "heightUnits", "weightUnits", "performanceStatus"
    ],
    "complications": ["patientId", "date", "lateComplicationOfTherapyDeveloped", "lateToxicityDetail", "suspectedTreatmentInducedNeoplasmDeveloped", "treatmentInducedNeoplasmDetails"],
    "consents": ["patientId", "consentId", "consentDate", "consentVersion", "patientConsentedTo", "reasonForRejection",
        "wasAssentObtained", "dateOfAssent", "assentFormVersion", "ifAssentNotObtainedWhyNot", "reconsentDate", "reconsentVersion",
        "consentingCoordinatorName", "previouslyConsented", "nameOfOtherBiobank", "hasConsentBeenWithdrawn",
        "dateOfConsentWithdrawal", "typeOfConsentWithdrawal", "reasonForConsentWithdrawal", "consentFormComplete"
    ]
}
alertCloser();

let endpoints = ["patients", "enrollments", "treatments", "samples", "diagnoses", "tumourboards", "outcomes", "complications", "consents"];
let types = ["bar", "column", "pie", "scatter"]
let type1 = types[Math.floor(Math.random() * types.length)];
let type2 = types[Math.floor(Math.random() * types.length)];

$("#table1").off("change").change(function() {
    document.getElementById("key1").innerHTML = "";
    selectPopulator("key1", categories[$("#table1").val()]);
});

$("#table2").off("change").change(function() {
    document.getElementById("key2").innerHTML = "";
    selectPopulator("key2", categories[$("#table2").val()]);
});

$("#adv1_confirm").off('click').click(function() {
    document.getElementById("adv1").innerHTML = '<div class="loader_bar"></div>';
    makeRequest($("#table1").val() + "/search", {
        "datasetId": datasetId
    }).then(function(response) {
        var data = JSON.parse(response)["results"][$("#table1").val()];
        var selectedKey = $("#key1").val()

        if (data[0][selectedKey] == undefined) {
            document.getElementById("adv1").innerHTML = "<p class='noPermission'>You don't have access to this data.</p>";
        } else {
            var count = groupBy(data, selectedKey);
            singleLayerDrawer("adv1", $("#type1").val(), "Distribution of " + splitString(selectedKey), currentDatasetName + " " + splitString($("#table1").val()), count)
        }
    })
});

$("#adv2_confirm").off('click').click(function() {
    document.getElementById("adv2").innerHTML = '<div class="loader_bar"></div>';
    makeRequest($("#table2").val() + "/search", {
        "datasetId": datasetId
    }).then(function(response) {
        var data = JSON.parse(response)["results"][$("#table2").val()];
        var selectedKey = $("#key2").val()

        if (data[0][selectedKey] == undefined) {
            document.getElementById("adv2").innerHTML = "<p class='noPermission'>You don't have access to this data.</p>";
        } else {
            var count = groupBy(data, selectedKey);
            singleLayerDrawer("adv2", $("#type2").val(), "Distribution of " + splitString(selectedKey), currentDatasetName + " " + splitString($("#table1").val()), count)
        }
    })
});

function initialize() {
    if (selectPopulated == 0) {
        selectPopulator("table1", endpoints);
        selectPopulator("table2", endpoints);
        selectPopulator("key1", categories["patients"]);
        selectPopulator("key2", categories["patients"]);
        selectPopulator("type1", types);
        selectPopulator("type2", types);
        selectPopulated = 1;

        document.getElementById("key1").selectedIndex = "6";
        document.getElementById("key2").selectedIndex = "6";
        document.getElementById("type1").selectedIndex = JSON.stringify(types.indexOf(type1));
        document.getElementById("type2").selectedIndex = JSON.stringify(types.indexOf(type2));

        makeRequest("patients/search", {
            "datasetId": datasetId
        }).then(function(response) {
            var data = JSON.parse(response)["results"]["patients"];
            var selectedKey = "provinceOfResidence"
            var count = groupBy(data, selectedKey);

            singleLayerDrawer("adv1", type1, "Distribution of Province Of Residence", currentDatasetName + " " + "Patients", count)
            singleLayerDrawer("adv2", type2, "Distribution of Province Of Residence", currentDatasetName + " " + "Patients", count)
        });
    }
}

function reloadGraphs() {
    document.getElementById('adv1_confirm').click();
    document.getElementById('adv2_confirm').click();
}

function selectPopulator(id, array) {
    let selectId = document.getElementById(id);

    for (let i = 0; i < array.length; i++) {
        selectId.options[selectId.options.length] = new Option(splitString(array[i]), array[i])
    }
}

// Capitalize the first letter of a string
function splitString(newString) {
    let splitted = newString.replace(/([a-z])([A-Z])/g, '$1 $2')
    let capitalized = splitted.charAt(0).toUpperCase() + splitted.substr(1);
    return capitalized;
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

function singleLayerDrawer(id, type, title, subtitle, count) {
    var categories = Object.keys(count);
    var values = Object.values(count);
    var seriesArray = highChartSeriesObjectMaker(categories, values);

    Highcharts.chart(id, {
        chart: {
            type: type,
            zoomType: 'xy'
        },
        credits: {
            enabled: false
        },
        title: {
            text: title
        },
        subtitle: {
            text: subtitle
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