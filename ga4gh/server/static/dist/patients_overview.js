"use strict";$(window).on("load",function(){makeRequest("datasets/search",{}).then(function(a){const b=JSON.parse(a),c=b.results.datasets;let d=document.getElementById("dropdown-menu");for(let b=0;b<c.length;b++)finalDatasetId.includes(c[b].id)||(finalDatasetId.push(c[b].id),finalDatasetName.push(c[b].name));for(let b=0;b<finalDatasetId.length;b++)d.innerHTML+="<a class=\"dropdown-item\" id=\"refresh\" href=\"javascript:void(0)\" onclick=\"refreshDataset("+b+")\">"+finalDatasetName[b]+"</a>";null==getCookie("datasetId")||-1==finalDatasetId.indexOf(getCookie("datasetId"))?(datasetId=finalDatasetId[0],setCookie("datasetId",datasetId),$("#dropdownMenuLink").html("<i class=\"fas fa-database\"></i> "+finalDatasetName[0])):(datasetId=getCookie("datasetId"),$("#dropdownMenuLink").html("<i class=\"fas fa-database\"></i> "+finalDatasetName[finalDatasetId.indexOf(datasetId)])),patient_main()},function(){alertBuilder("No data currently available. Please contact a system administrator for assistance.")})});function refreshDataset(a){datasetId=finalDatasetId[a],document.getElementById("warningMsg").style.display="none",setCookie("datasetId",datasetId),$("#dropdownMenuLink").html("<i class=\"fas fa-database\"></i> "+finalDatasetName[finalDatasetId.indexOf(getCookie("datasetId"))]),patient_main()}var patientStatusCode=0;let loader="<div class=\"loader_bar\"></div>";document.getElementById("raceGraph").innerHTML="<div class=\"loader_bar\"></div>",document.getElementById("genderGraph").innerHTML="<div class=\"loader_bar\"></div>",document.getElementById("provinceGraph").innerHTML="<div class=\"loader_bar\"></div>";function replace_undefined(a){for(let b=0;b<a.length;b++)("undefined"==a[b]||null==a[b])&&(a[b]="N/A");return a}function patient_main(){if(""!=document.getElementById("patients_table").innerHTML){try{var a=$("#patients_table").DataTable();a.destroy()}catch(a){}document.getElementById("patients_table").innerHTML=""}if(""!=document.getElementById("mergedTreatmentsDiagnosesTable").innerHTML){try{var a=$("#mergedTreatmentsDiagnosesTable").DataTable();a.destroy()}catch(a){}document.getElementById("mergedTreatmentsDiagnosesTable").innerHTML=""}var b=[],c=[],d=[];makeRequest("patients/search",{datasetId:datasetId}).then(function(a){var e=JSON.parse(a),f=e.results.patients,g=$("<table/>").attr("id","patients_table");$("#patients_table").append("<thead><tr><th scope=\"col\">Patient ID</th><th scope=\"col\">Gender</th><th scope=\"col\">Date of Death</th><th scope=\"col\">Province of Residence</th> <th scope=\"col\">Date of Birth</th><th scope=\"col\">Race</th><th scope=\"col\">Occupational Or Environmental Exposure</th></tr></thead><tbody>");for(var h=0;h<f.length;h++){b.push(f[h].race),c.push(f[h].provinceOfResidence),d.push(f[h].gender);var j="<td scope=\"col\">"+f[h].patientId+"</td>",k="<td scope=\"col\">"+f[h].gender+"</td>",l="<td scope=\"col\">"+f[h].dateOfDeath+"</td>",m="<td scope=\"col\">"+f[h].provinceOfResidence+"</td>",n="<td scope=\"col\">"+f[h].dateOfBirth+"</td>",o="<td scope=\"col\">"+f[h].race+"</td>",p="<td scope=\"col\">"+f[h].occupationalOrEnvironmentalExposure+"</td>",q=("<tr>"+j+k+l+m+n+o+p+"</tr>").replace(/undefined/g,"N/A");$("#patients_table").append(q)}b=replace_undefined(b),c=replace_undefined(c),d=replace_undefined(d),categoriesDrawer("raceGraph","Ethnic Groups",b),categoriesDrawer("provinceGraph","Provinces",c),categoriesDrawer("genderGraph","Genders",d),$("#patients_table").append("</tbody><tfoot><tr><th scope=\"col\">Patient ID</th><th scope=\"col\">Gender</th><th scope=\"col\">Date of Death</th><th scope=\"col\">Province of Residence</th> <th scope=\"col\">Date of Birth</th><th scope=\"col\">Race</th><th scope=\"col\">OEE</th></tr></tfoot>"),$(document).ready(function(){try{$("#patients_table").DataTable({initComplete:function(){this.api().columns().every(function(){var a=this,b=$("<select><option value=\"\"></option></select>").appendTo($(a.footer()).empty()).on("change",function(){$.fn.dataTable.util.escapeRegex($(this).val());a.search("^"+this.value,!0,!1,!0).draw()});a.data().unique().sort().each(function(a){b.append("<option value=\""+a+"\">"+a+"</option>")})})}})}catch(a){alertBuilder("The table wasn't correctly rendered. Please refresh the page.")}}),$("#patients_table tbody").off("click").on("click","tr",function(){var a=$("#patients_table").DataTable(),b=a.row(this).data()[0];"N/A"==b?alertBuilder("We are sorry, but the record you are trying to query doesn't have a valid id."):patientInfoFetcher(b)})},function(){noPermissionMessage("raceGraph"),noPermissionMessage("provinceGraph"),noPermissionMessage("genderGraph")})}function noPermissionMessage(a){document.getElementById(a).innerHTML="<p class='noPermission'>No data available</p>"}function highChartSeriesObjectMaker(a,b){for(var c={},d=[],e=0;e<a.length;e++)c={},c.name=a[e],c.y=b[e],d.push(c);return d}function categoriesDrawer(a,b,c){var d=Object.keys(categoriesCounter(c)),e=Object.values(categoriesCounter(c)),f=highChartSeriesObjectMaker(d,e);drillDownDrawer(a,b,d,"",f,[])}function categoriesCounter(a){for(var b={},c=0;c<a.length;c++)b[a[c]]||(b[a[c]]=0),b[a[c]]++;return b}function drillDownDrawer(a,b,c,d,e,f){var g="";Highcharts.chart(a,{chart:{type:"pie",style:{fontFamily:"Roboto"}},title:{text:b},credits:{enabled:!1},exporting:{enabled:!1},xAxis:{categories:c},legend:{enabled:!1},plotOptions:{pie:{allowPointSelect:!0,depth:35,dataLabels:{enabled:!0},point:{events:{click:function(){g==this.name?g==this.name&&($("#patients_table").DataTable().search("").draw(),g=""):($("#patients_table").DataTable().search(this.name).draw(),g=this.name)}}}}},series:[{name:d,colorByPoint:!0,data:e}],drilldown:{series:f}})}function patientInfoFetcher(a){if(1==patientStatusCode){try{var b=$("#mergedTreatmentsDiagnosesTable").DataTable();b.destroy()}catch(a){}document.getElementById("mergedTreatmentsDiagnosesTable").innerHTML=""}var c=new XMLHttpRequest;c.open("POST",prepend_path+"/samples/search",!0),c.setRequestHeader("Content-Type","application/json"),c.setRequestHeader("Accept","application/json"),c.setRequestHeader("Authorization","Bearer "+session_id),c.send(JSON.stringify({datasetId:datasetId,filters:[{field:"patientId",operator:"==",value:a}]})),c.onload=function(){var b=JSON.parse(this.responseText),d=b.results.samples;c.open("POST",prepend_path+"treatments/search",!0),c.setRequestHeader("Content-Type","application/json"),c.setRequestHeader("Accept","application/json"),c.setRequestHeader("Authorization","Bearer "+session_id),c.send(JSON.stringify({datasetId:datasetId,filters:[{field:"patientId",operator:"==",value:a}]})),c.onload=function(){var a=JSON.parse(this.responseText),b=a.results.treatments,c=$("<table/>").attr("id","mergedTreatmentsDiagnosesTable");$("#mergedTreatmentsDiagnosesTable").append("<thead><tr><th scope=\"col\">Patient ID</th><th scope=\"col\">Collection Hospital</th><th scope=\"col\">Collection Date</th><th scope=\"col\">Cancer Type</th><th scope=\"col\">Response to treatment</th><th scope=\"col\">Drug list</th><th scope=\"col\">Therapeutic Modality </th></tr></thead><tbody>");for(var e=0;e<d.length;e++){var f="<td scope=\"col\">"+d[e].patientId+"</td>",g="<td scope=\"col\">"+d[e].collectionHospital+"</td>",h="<td scope=\"col\">"+d[e].collectionDate+"</td>",j="<td scope=\"col\">"+d[e].cancerType+"</td>",k="<td scope=\"col\">"+b[e].responseToTreatment+"</td>",l="<td scope=\"col\">"+b[e].drugListOrAgent+"</td>",m="<td scope=\"col\">"+b[e].therapeuticModality+"</td>",n=("<tr>"+f+g+h+j+k+l+m+"</tr>").replace(/undefined/g,"N/A");$("#mergedTreatmentsDiagnosesTable").append(n)}$("#mergedTreatmentsDiagnosesTable").append("</tbody>"),$(document).ready(function(){$("#mergedTreatmentsDiagnosesTable").DataTable(),patientStatusCode=1})}}}