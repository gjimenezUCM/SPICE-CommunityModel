'use strict';
const db = require("../models");

const LogsDAO = db.logs;

/**
 * Logs
 * Access to CM logs
 *
 * returns logs documents
 **/

exports.getAllLogs = function (logsType) {
    return new Promise(function (resolve, reject) {
        LogsDAO.allLogs(logsType,
        data => {
            resolve(data)
        },
            error => {
                console.log("LogsService error: " + error);
                reject(error)
            }
    )
    });
};

exports.getNLatestLogs = function (n, logsType) {
    return new Promise(function (resolve, reject) {
        LogsDAO.nLatestLogs(n, logsType,
            data => {
                resolve(data)
            },
            error => {
                console.log("LogsService error: " + error);
                reject(error)
            })
    });
};

exports.getLogsBetweenTwoDates = function (startDate, endDate, logsType) {
    return new Promise(function (resolve, reject) {
        LogsDAO.logsBetweenTwoDates(startDate, endDate, logsType,
            data => {
                resolve(data)
            },
            error => {
                console.log("LogsService error: " + error);
                reject(error)
            })
    });
};

