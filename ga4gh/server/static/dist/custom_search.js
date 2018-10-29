"use strict";

let advanced_search_select_populated = 0;
$("a[href='#custom_search']").on('shown.bs.tab', function (e) {
  window.history.pushState("", "Custom Search", "#custom_search");
  activeTab = e.target;
  var tableIds = ["patients", "enrollments", "treatments", "samples", "diagnoses", "tumourboards", "outcomes", "complications", "consents"];
  var operators = [">", "<", "==", ">=", "<=", "is"];
  var components = [];
  let newRequest = {};

  if (advanced_search_select_populated == 0) {
    selectPopulator("ads_table", tableIds);
    selectPopulator("ads_key", categories[tableIds[0]]);
    selectPopulator("ads_operator", operators);
    selectPopulator("ads_require", ["required", "optional"]);
    selectPopulator("ads_output", tableIds);
    advanced_search_select_populated = 1;
  }

  $("#ads_table").change(function () {
    document.getElementById("ads_key").innerHTML = "";
    selectPopulator("ads_key", categories[$("#ads_table").val()]);
  });

  function selectPopulator(id, array) {
    let selectId = document.getElementById(id);

    for (let i = 0; i < array.length; i++) {
      selectId.options[selectId.options.length] = new Option(array[i], array[i]);
    }
  }

  $("#ads_add").click(function () {
    if ($("#ads_input").val() != "") {
      addComponent();
    } else {
      alertBuilder("Please specify input value");
    }
  }); //    document.getElementById("ads_add").addEventListener("click", addComponent);
  // Add a new component

  function addComponent() {
    document.getElementById("success-alert").style.display = "block";
    $("#success-alert").fadeTo(1000, 500).slideUp(500, function () {
      $("#success-alert").slideUp(500);
    });
    let component = {};
    component[$("#ads_table").val()] = {};
    component[$("#ads_table").val()]["filters"] = [];
    let filter = {};
    filter["field"] = $("#ads_key").val();
    filter["operator"] = $("#ads_operator").val();
    filter["value"] = $("#ads_input").val();
    component[$("#ads_table").val()]["filters"].push(filter);
    component["required"] = $("#ads_require").val();
    component["id"] = JSON.stringify(components.length);
    console.log(component);
    components.push(component);
  } //document.getElementById("ads_submit"),addEventListener("click", submitRequest);
  //    $( "#ads_check" ).click(function() {
  //        confirm("Here are the existing components" + JSON.stringify(components))
  //    });


  $("#ads_submit").click(function () {
    submitRequest();
  });

  function submitRequest() {
    newRequest = {}; //        let logic = {"and": [{"and": []}, {"or": []}]}
    //
    //        for (let i = 0; i < components.length; i++) {
    //
    //            if (components[i]["required"] == "required") {
    //                logic["and"][0]["and"].push({"id": components[i]["id"]});
    //            }
    //            else logic["and"][1]["or"].push({"id": components[i]["id"]});
    //        }
    //
    //        if (logic["and"][0]["and"].length == 0) {
    //            delete logic["and"][0]["and"];
    //        }
    //
    //        else if (logic["and"][1]["or"].length == 0) {
    //            delete logic["and"][1]["or"];
    //        }

    let logic = {
      "and": []
    };

    for (let i = 0; i < components.length; i++) {
      logic["and"].push({
        "id": components[i]["id"]
      });
    }

    let results = [{
      "table": $("#ads_output").val()
    }];
    newRequest["dataset_id"] = datasetId;
    newRequest["logic"] = logic;
    newRequest["components"] = components;
    newRequest["results"] = results;
    console.log(newRequest);
    makeRequest("/search", newRequest).then(function (response) {
      document.getElementById("resultTable").innerHTML = "";
      gridMaker(JSON.parse(response), $("#ads_output").val());
    });
  }

  function gridMaker(results, endpoint) {
    var extrationDataset = results['results'][endpoint];
    var keyList = Object.keys(extrationDataset[0]);
    var columnDefs = [];
    var newHeader;
    var hiddenHeaders = ["id", "datasetId", "name"];
    console.log(extrationDataset);

    for (var i = 0; i < keyList.length; i++) {
      newHeader = {};

      if (!hiddenHeaders.includes(keyList[i])) {
        newHeader["headerName"] = keyList[i];
        newHeader["field"] = keyList[i];
        columnDefs.push(newHeader);
      }
    }

    columnDefs[0]["checkboxSelection"] = true; //enable checkbox

    columnDefs[0]["headerCheckboxSelection"] = true; //enable top level selector

    var gridOptions = {
      columnDefs: columnDefs,
      rowData: extrationDataset,
      enableSorting: true,
      enableFilter: true,
      rowSelection: "multiple",
      enableColResize: true
    };
    var eGridDiv = document.querySelector('#resultTable');
    new agGrid.Grid(eGridDiv, gridOptions);
  } //    $( "#advanced_search_table_selector" ).change(function() {
  //        document.getElementById("currSearchTable").innerHTML = "";
  //        // tableBuilder($("#advanced_search_table_selector").val(), "currSearchTable");
  //    });
  //    function tableBuilder(table, id) {
  //        let listOfHeaders = categories[table];
  //        let columnDefs = []
  //        let rowData = []
  //
  //        var newColumnDefs = [{"headerName": "Attributes", "field": "field", width: 500}, {"headerName": "Filter", "field": "value", "width": 250}];
  //
  //        for (var j = 0; j < listOfHeaders.length; j++) {
  //            var tempItem = {};
  //            tempItem["field"] = listOfHeaders[j].replace(/([a-z])([A-Z])/g, '$1 $2');
  //            tempItem["value"] = "test"
  //            rowData.push(tempItem);
  //        }
  //        gridMaker(newColumnDefs, rowData, id);
  //    }
  //
  //    var gridOptions;
  //
  //    function gridMaker(newColumnDefs, newDataset, id){
  //
  //        gridOptions = {
  //            domLayout: 'autoHeight',
  //            columnDefs: newColumnDefs,
  //            rowData: newDataset,
  //            enableSorting: true,
  //            rowSelection: "single",
  //            enableColResize: true,
  //            onSelectionChanged: onSelectionChanged
  //        };
  //
  //        var eGridDiv = document.querySelector('#' + id);
  //        new agGrid.Grid(eGridDiv, gridOptions);
  //    }
  //
  //    function onSelectionChanged() {
  //        var selectedRows = gridOptions.api.getSelectedRows();
  //        console.log(selectedRows)
  //        window.alert(selectedRows[0].field);
  //    }
  // Get the modal


  var modal = document.getElementById('myModal'); // Get the button that opens the modal

  var btn = document.getElementById("ads_check"); // Get the <span> element that closes the modal

  var span = document.getElementsByClassName("close")[0]; // When the user clicks on the button, open the modal

  btn.onclick = function () {
    modal.style.display = "block";
    document.getElementById("modal_text").innerHTML = JSON.stringify(components);
  }; // When the user clicks on <span> (x), close the modal


  span.onclick = function () {
    modal.style.display = "none";
  }; // When the user clicks anywhere outside of the modal, close it


  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
});