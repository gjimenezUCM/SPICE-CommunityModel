'use strict';

const db = require("../models");
const SimilarityDAO = db.similarities;

/**
 * Dissimilarity between two communities
 * Returns the dissimilarity score between two communities
 *
 * communityId Long ID of the target community to compute dissimilarity
 * otherCommunityId Long ID of the other community to compute dissimilarity
 * returns similarityScore
 **/
exports.computeDissimilarity = function (targetCommunityId, otherCommunityId) {
  return new Promise(function (resolve, reject) {
    let result = {};
    if (targetCommunityId === otherCommunityId) {
        reject("targetCommunityId === otherCommunityId");
    }
    SimilarityDAO.getByIds(targetCommunityId, otherCommunityId,
      data => {
        // TODO: Dissimilarity must be computed in Community Model
        data.value = 1 - data.value;
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
 * K-most dissimilar communities
 * Returns a list with the k most dissimilar communities to the chosen one in the model.
 *
 * communityId Long ID of the target community to compute dissimilarity
 * k Integer Size of the result (k most dissimilar communities)
 * returns similarityScore
 **/
exports.computeKmostDissimilar = function (communityId, k) {
  return new Promise(function (resolve, reject) {
    let result = {};
    SimilarityDAO.allForId(communityId,
      data => {
        // TODO: Dissimilarity must be computed in Community Model
        data.forEach((element) => {
          element.value = 1 - element.value;
        });
        data.reverse();
        result['application/json'] = data.slice(0, k);
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
}


/**
 * K-most similar communities
 * Returns a list with the k most similar communities to the chosen one in the model.
 *
 * communityId Long ID of the target community to compute similarity
 * k Integer Size of the result (k most similar communities)
 * returns similarityScore
 **/
exports.computeKmostSimilar = function (communityId, k) {
  return new Promise(function (resolve, reject) {
    let result = {};
    SimilarityDAO.allForId(communityId,
      data => {
        result['application/json'] = data.slice(0, k);
        if (Object.keys(result).length > 0) {
          resolve(result[Object.keys(result)[0]]);
        }
        // else if(Object.keys(result).length === 1){
        //
        // }
        else {
          resolve();
        }
      },
      error => {
        reject(error);
      }
    );
  });

  //   return new Promise(function(resolve, reject) {
  //     var examples = {};
  //     examples['application/json'] = [ {
  //   "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  //   "similarity-function" : "similarity-function",
  //   "value" : 0.8008281904610115
  // }, {
  //   "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  //   "similarity-function" : "similarity-function",
  //   "value" : 0.8008281904610115
  // } ];
  //     if (Object.keys(examples).length > 0) {
  //       resolve(examples[Object.keys(examples)[0]]);
  //     } else {
  //       resolve();
  //     }
  //   });
}


/**
 * Similarity between two communities
 * Returns a similarity score between two communities.
 *
 * communityId Long ID of the target community to compute similarity
 * otherCommunityId Long ID of the other community to compute similarity
 * returns similarityScore
 **/
exports.computeSimilarity = function (targetCommunityId, otherCommunityId) {
  return new Promise(function (resolve, reject) {
    let result = {};
      if (targetCommunityId === otherCommunityId) {
          reject("targetCommunityId === otherCommunityId");
      }
    SimilarityDAO.getByIds(targetCommunityId, otherCommunityId,
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
//   return new Promise(function(resolve, reject) {
//     var examples = {};
//     examples['application/json'] = [ {
//   "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
//   "similarity-function" : "similarity-function",
//   "value" : 0.8008281904610115
// }, {
//   "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
//   "similarity-function" : "similarity-function",
//   "value" : 0.8008281904610115
// } ];
//     if (Object.keys(examples).length > 0) {
//       resolve(examples[Object.keys(examples)[0]]);
//     } else {
//       resolve();
//     }
//   });

