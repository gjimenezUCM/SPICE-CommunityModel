'use strict';

var requests = require('./helpers/redirectRequest.js');


exports.getDump = function () {
    return requests.getData("/dump");
}


/**
 * Redirect post request to CM model to load data into mongoDB
 */
exports.postLoad = function (body) {
    return requests.postData(body, "/load");

}