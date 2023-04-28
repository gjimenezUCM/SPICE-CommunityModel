const idParam = 'perspectiveId';
const Perspectives = require('../service/perspectivesService.js');
const Flags = require('../service/flagsService.js');
const JobManager = require('./jobsRoute/jobsManager.js');

// check if flag exist
// if exist then update CM
// if !exist then access DB
module.exports.getPerspectives = function getPerspectives(req, res, next) {
    Flags.getFlags()
        .then(function (response) {
            if (response == null) {
                Perspectives.getPerspectives()
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send("invalid perspective id");
                    });
            } else {
                JobManager.createJob(0, "getPerspectives")
                    .then(function (path) {
                        res.status(202).send(path);
                    })
                    .catch(function (error) {
                        res.status(400).send(error);
                    });
            }
        })
        .catch(function (response) {
            console.error("Perspectives.getPerspectives -> Flags.getFlags: error: " + response)
        });
};

// check if flag exist
// if exist then update CM
// if !exist then access DB
module.exports.getPerspectiveById = function getPerspectiveById(req, res, next) {
    const perspectiveId = req.params[idParam];
    Flags.getFlagById(perspectiveId)
        .then(function (response) {
            if (response == null) {
                Perspectives.getPerspectiveById(perspectiveId)
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send("invalid perspective id");
                    });
            } else {
                JobManager.createJob(perspectiveId, "getPerspectiveById")
                    .then(function (path) {
                        res.status(202).send(path);
                    })
                    .catch(function (error) {
                        res.status(400).send(error);
                    });
            }
        })
        .catch(function (response) {
            console.error("Perspectives.getPerspectiveById -> Flags.getFlagById: error: " + response)
        });
};

module.exports.listPerspectiveCommunities = function listPerspectiveCommunities(req, res, next) {
    const perspectiveId = req.params[idParam];

    // Check flag, if exist then access mongodb and return data
    // if false then check if perspective exist, create new job and return 202, and a link to that job
    Flags.getFlagById(perspectiveId)
        .then(function (response) {
            if (response == null) { // flag does not exist => no update needed
                Perspectives.listPerspectiveCommunities(perspectiveId)
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send("invalid perspective id");
                    });
            } else { //flag exist
                JobManager.createJob(perspectiveId, "listPerspectiveCommunities")
                    .then(function (path) {
                        res.status(202).send(path);
                    })
                    .catch(function (error) {
                        res.status(400).send(error);
                    });
            }
        })
        .catch(function (response) {
            console.error("Perspectives.listPerspectiveCommunities -> Flags.getFlagById: error: " + response)
        });
};

// redirect post request to api_loader
module.exports.postPerspective = function postPerspective(req, res, next) {
    try {

        Perspectives.getPerspectiveById(req.body.id)
            .then(function (response) { // Perspective with that id exists
                res.status(409).send({insertedPerspectiveId: "-Error, perspective already exist-"});
            })
            .catch(function (error) { // Perspective with that id doesnt exist (it can be inserted)
                Perspectives.PostPerspective(req.body)
                    .then(function (perspectiveId) {
                        var response = {insertedPerspectiveId: perspectiveId};
                        res.status(202).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send(response);
                    });
            });
    } catch (error) {
        console.error(error);
    }
};

module.exports.deletePerspective = function deletePerspective(req, res, next) {
    const perspectiveId = req.params[idParam];
    Perspectives.deletePerspective(perspectiveId)
        .then(function (response) {
            if (response === 404)
                res.status(404).send("Perspective with that id does not exist");
            else
                res.status(200).send("Perspective deleted");
        })
        .catch(function (error) {
            res.status(400).send(error);
        });
};