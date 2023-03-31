'use strict';
const db = require("../models");

const CommunitiesVisualizationDAO = db.communitiesVisualization;


exports.getIndex = function () {
  return new Promise(function (resolve, reject) {
    let result = {};
    CommunitiesVisualizationDAO.getIndex(
      data => {
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
* community description and explanation
* Returns information about a community
*
* communityId Long ID of community to return
* returns community
**/
exports.getById = function (id) {
  return new Promise(function (resolve, reject) {
    let result = {};
    CommunitiesVisualizationDAO.getById(id,
      data => {
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



