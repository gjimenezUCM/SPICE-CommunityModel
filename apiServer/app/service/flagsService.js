'use strict';
const db = require("../models");

const FlagDAO = db.flag;

/**
* Flags
* Access to specific flag to check it
* @param {String} type type of flags (default="withoutErrors")
* @returns flag document
**/
exports.getFlags = function (type = "withoutErrors") {
    if (type == "withoutErrors") {
        return new Promise(function (resolve, reject) {
            FlagDAO.checkFlagsWithoutErrors(
                data => {
                    resolve(data)
                },
                error => {
                    console.log("flagService error: " + error);
                    reject(error)
                })
        });
    }
    else {
        return new Promise(function (resolve, reject) {
            FlagDAO.checkFlags(
                data => {
                    resolve(data)
                },
                error => {
                    console.log("flagService error: " + error);
                    reject(error)
                })
        });
    }

};

exports.getFlagById = function (perspectiveId) {
    return new Promise(function (resolve, reject) {
        FlagDAO.checkFlagById(perspectiveId,
            data => {
                resolve(data)
            },
            error => {
                console.log("flagService error: " + error);
                reject(error)
            })
    });
};

exports.removeFlag = function (flagId) {
    return new Promise(function (resolve, reject) {
        FlagDAO.removeFlagById(flagId,
            data => {
                resolve(data)
            },
            error => {
                console.log("flagService error: " + error);
                reject(error)
            })
    });
};

