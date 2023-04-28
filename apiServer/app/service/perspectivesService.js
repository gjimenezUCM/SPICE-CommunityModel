'use strict';
const db = require("../models");
var redirect = require('./helpers/redirectRequest.js');

const PerspectiveDAO = db.perspectives;
const CommunityDAO = db.communities;
const UsersDAO = db.users;
const FlagDAO = db.flag;


/**
 * Perspectives in the model
 * Access to a list of the Perspectives
 *
 * returns List
 **/
exports.getPerspectives = function () {
    return new Promise(function (resolve, reject) {

        let result = {};
        PerspectiveDAO.all((perspectives) => {
            result['application/json'] = perspectives;
            if (Object.keys(result).length > 0) {
                resolve(result[Object.keys(result)[0]]);
            } else {
                resolve();
            }
        });
    });

};


/**
 * Returns information about a perspective
 *
 * perspectiveId Long ID of perspective to return
 * returns perspective
 **/
exports.getPerspectiveById = function (perspectiveId) {
    return new Promise(function (resolve, reject) {

        let result = {};
        PerspectiveDAO.getById(perspectiveId,
            data => {
                // console.log(data)
                result['application/json'] = data;
                if (Object.keys(result).length > 0) {
                    resolve(result[Object.keys(result)[0]]);
                } else {
                    resolve();
                }
            },
            error => {
                reject(error);
            }
        );
    });
};


/**
 * Returns list with communities that have the same perspectiveId
 *
 * perspectiveId Long ID of perspective
 * returns List
 **/
exports.listPerspectiveCommunities = function (perspectiveId) {
    return new Promise(function (resolve, reject) {
        // obtains all communities and then filter them by perspectiveId
        let result = {};
        let data = []
        let communities = {};
        CommunityDAO.all((com) => {
            communities = com;
            if (communities.length == 0) {
                resolve();
            }

            for (var i = 0; i < communities.length; i++) {
                var community = communities[i]
                if (community.perspectiveId == perspectiveId) {
                    data.push(community);
                }
            }
            // communities.forEach(element => {
            //   var community = JSON.parse(element);
            //   console.log(community);
            //   if (community.perspective == perspectiveId) {
            //     data.push(communities);
            //   }
            // });

            result['application/json'] = data;
            if (Object.keys(result).length > 0) {
                resolve(result[Object.keys(result)[0]]);
            } else {
                resolve();
            }
        });

    });
};


/**
 * Redirects POST request to api_loader
 * Used to inform the community model about new perspectives
 *
 * body perspective object that will be added to the model
 * no response value expected for this operation
 */
exports.PostPerspective = function (body) {
    try {
        console.log("perspective service - post perspective")
        console.log(body)
        console.log("\n")

        return new Promise(function (resolve, reject) {
            // insert perspective
            PerspectiveDAO.insertPerspective(body,
                data => {
                    resolve(data);
                },
                error => {
                    console.error("PostPerspective-PerspectiveDAO.insertPerspective error: " + error);
                    reject(error)
                })
        })
            .then((perspectiveId) => {
                // create flag
                var json = {
                    perspectiveId: perspectiveId,
                    userid: "flagAllUsers",
                    needToProcess: true,
                    error: "N/D"
                };
                FlagDAO.insertFlag(json,
                    data => {
                    },
                    error => {
                        console.log("PostPerspective-FlagDAO.insertFlag perspective error: " + error);
                    })

                // post cm
                return redirect.postData(perspectiveId, "/perspective");
            })
            .catch(function (error) {
                console.error("PerspectiveDAO.insertPerspective.promise1: " + error);
            });
    } catch (error) {
        console.log("PostPerspective error:" + error);
    }
}

/**
 * Perspectives in the model
 * Access to a list of the Perspectives
 *
 * returns List
 **/
exports.deletePerspective = function (perspectiveId) {
    // return new Promise(function (resolve, reject) {
        return redirect.deleteData(perspectiveId, "/perspective");
    // });

};