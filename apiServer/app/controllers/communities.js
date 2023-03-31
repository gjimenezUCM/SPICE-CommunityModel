const idParam = 'communityId';
const Communities = require('../service/communitiesService.js');
const Flags = require('../service/flagsService.js');
const JobManager = require('./jobsRoute/jobsManager.js');

module.exports.getCommunities = function getCommunities(req, res, next) {
  Flags.getFlags()
    .then(function (response) {
      if (response == null) {
        Communities.getCommunities()
          .then(function (response) {
            res.status(200).send(response);
          })
          .catch(function (response) {
            res.status(400).send(response);
          });
      }
      else {
        JobManager.createJob(0, "getCommunities")
          .then(function (path) {
            res.status(202).send(path);
          })
          .catch(function (error) {
            res.status(400).send(error);
          });
      }
    })
    .catch(function (response) {
      console.error("Communities.getCommunities -> Flags.getFlags: error: " + response)
    });
};

module.exports.getCommunityById = function getCommunityById(req, res, next) {
  const communityId = req.params[idParam];
  Communities.getCommunityById(communityId)
    .then(function (response) {
      var community = response
      Flags.getFlagById(community.perspectiveId)
        .then(function (flag) {
          if (flag == null) { // flag does not exist => no update needed
            res.status(200).send(community);
          }
          else { //flag exist
            JobManager.createJob(communityId, "getCommunityById")
              .then(function (path) {
                res.status(202).send(path);
              })
              .catch(function (error) {
                res.status(400).send(error);
              });
          }
        })
        .catch(function (response) {
          console.error("Communities.getCommunityById -> Flags.getFlagById: error: " + response)
        });
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};

module.exports.listCommunityUsers = function listCommunityUsers(req, res, next) {
  const communityId = req.params[idParam];
  //get users list
  Communities.listCommunityUsers(communityId)
    .then(function (response) {
      var users = response;
      //get community
      Communities.getCommunityById(communityId)
        .then(function (response) {
          var community = response;
          Flags.getFlagById(community.perspectiveId)
            .then(function (flag) {
              if (flag == null) { // flag does not exist => no update needed
                res.status(200).send(users);
              }
              else { //flag exist
                JobManager.createJob(communityId, "listCommunityUsers")
                  .then(function (path) {
                    res.status(202).send(path);
                  })
                  .catch(function (error) {
                    res.status(400).send(error);
                  });
              }
            })
            .catch(function (response) {
              console.error("Communities.listCommunityUsers -> Flags.getFlagById: error: " + response)
            });
        })
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};
