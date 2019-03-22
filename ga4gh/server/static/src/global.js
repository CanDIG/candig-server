"use strict";

/**
 * Return the aggregation value of a key from an array of objects.
 * @param {array} objectArray: An array of objects.
 * @param {object} property: The key to aggregate on.
 * @return an object with different values of the queried property being the key, and frequency being the value.
*/
function groupBy(objectArray, property) {
    return objectArray.reduce(function(acc, obj) {
        var key = obj[property];
        if (!acc[key]) {
            acc[key] = 0;
        }
        acc[key] += 1;
        delete acc["undefined"]
        return acc;
    }, {});
}


/**
 * Make a request to the requested endpoint
 * @param {string} path: The path to send the query to.
 * @param {object} body: The body of the xhr request.
 * @return a Promise with a complete response from the server
*/
function makeRequest(path, body) {
    return new Promise(function(resolve, reject) {
        let results = []
        let key;

        // Initialize the request with empty pageToken
        return repeatRequest("");

        function repeatRequest(pageToken) {
            body["pageToken"] = pageToken;

            var xhr = new XMLHttpRequest();
            xhr.open('POST', prepend_path + path, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
            xhr.onload = function() {
                if (xhr.status == 200) {

                    let data = JSON.parse(xhr.response);

                    // If initial request completes the request, resolve with the raw response
                    if (data["results"]["nextPageToken"] == undefined && results.length == 0) {
                        resolve(xhr.response)
                    }

                    // If unsolved, search for the table name in the response
                    if (key == undefined) {
                        let keys = Object.keys(data["results"])

                        for (let i = 0; i < keys.length; i++) {
                            if (keys[i] != "nextPageToken" && keys[i] != "total") {
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
                    if (xhr.status == 403 || xhr.status == 401) {
                        alertBuilder("Your session might have expired. Click <a href='/'>here</a> to restore your session." +
                            " If problems persist, please contact your system administrators for assistance.");
                    } else if (xhr.status == 500) {
                        alertBuilder("Unexpected errors occurred. Click <a href='/'>here</a> to refresh your session." +
                            " If problems persist, please contact your system administrators for assistance.");
                    } else if (xhr.status == 404) {
                        alertBuilder("One or more resources you requested do not exist.");
                        resolve(xhr.response);
                    }
                    reject(Error(xhr.response));
                }

                stopLoading();
            };
            xhr.onerror = function() {
                reject(Error(xhr.response));
            };
            xhr.send(JSON.stringify(body));
        }
    })
};


function logout() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", prepend_path + "/logout_oidc", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('Authorization', 'Bearer ' + session_id);
    xhr.send('{}');
    xhr.onload = function() {
        window.location.href = logout_url;
    }
}

$('.alert').on('close.bs.alert', function(e) {
    // prevent the alert from being removed from DOM
    e.preventDefault();
    var warningMsg = document.getElementById('warningMsg');
    warningMsg.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>'
    warningMsg.style.display = "none";
});

function alertCloser() {
    var warningMsg = document.getElementById('warningMsg');
    warningMsg.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>'
    warningMsg.style.display = "none";
}

function alertBuilder(message) {
    let warningMsg = document.getElementById('warningMsg');
    warningMsg.style.display = "block";
    warningMsg.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>'
    warningMsg.innerHTML += message;
}

function startLoading() {
    document.getElementById("initial_loader").style.display = "block";
}

function stopLoading() {
    setTimeout(function() {
        document.getElementById("initial_loader").style.display = "None";
    }, 0);
}

function getCookie(name) {
    let cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        if (cookies[i].split("=")[0] == name) {
            return cookies[i].split("=")[1];
        }
    }
    return null;
}

function setCookie(name, value) {
    document.cookie = name + "=" + value;
}

// Sugur-coated complexRequestHelper for /search request
function searchRequest(table, keys, datasetId, filter = {}, returnTable) {
    return complexRequestHelper(table, keys, datasetId, filter, false, returnTable)
}

// Sugur-coated complexRequestHelper for /count request
function countRequest(table, keys, datasetId, filter = {}) {
    return complexRequestHelper(table, keys, datasetId, filter, true, table)
}


/**
 * Make a simple one-component request to the /count or /search endpoint
 * @param {string} table: The table of the request
 * @param {array} keys: A list of fields to aggregate on or return
 * @param {string} datasetId: The current chosen datasetId 
 * @param {object} filter: An object that contains filter, defaults to empty.
 * @param {boolean} requestCount: When it's true, make request to /count, otherwise to /search. Defaults to true.
 * @param {string} returnTable: The table that is requested to return.
 * @return a Promise with an object that contains aggregation or filtered values from the server
*/
function complexRequestHelper(table, keys, datasetId, filter = {}, requestCount = true, returnTable) {
    return new Promise(function(resolve, reject) {

    // Default endpoint is count unless otherwise specified.
    let endpoint = "/count"

    let body = {
        "dataset_id": datasetId,
        "logic": {
            "id": "A"
        },
        "components": [
            {
                "id": "A"
            }
        ],
        "results": [
            {
                "table": returnTable,
                "fields": keys
            }
        ]
    }
    // Assign the requested table to be the key of the first component
    body["components"][0][table] = {}

    // If filter is specified
    if (Object.keys(filter).length != 0){
        body["components"][0][table]["filters"] = []
        body["components"][0][table]["filters"].push(filter)
    }

    // If a query to the /search endpoint is specified
    if (!requestCount) {
        endpoint = "/search"
    }

    makeRequest(endpoint, body).then(function(response) {

        if (endpoint == "/count") {
            let listOfCounts = JSON.parse(response)["results"][returnTable][0];
            resolve(listOfCounts);
        }

        else resolve(JSON.parse(response)["results"][returnTable]);

    }), function(Error) {

        reject(Error(response));
        
    }
})}

