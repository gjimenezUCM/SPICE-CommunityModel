'use strict';

const idParam_fileId = 'fileId';

const SeedFileConfig = require("../config/seedFile.config.js");
const Flags = require("../service/flagsService");
const CommunitiesVis = require("../service/communitiesVisualizationService");
const JobManager = require("./jobsRoute/jobsManager");


module.exports.getSeed = function getSeed(req, res, next) {
    let seedFile = require('../src/' + SeedFileConfig.filename);
    // console.log(seedFile);
    res.status(200).send(seedFile);
};


// router.get('/files', function (req, res, next) {
module.exports.getIndex = function getIndex(req, res, next) {
    Flags.getFlags()
        .then(function (response) {
            if (response == null) {
                CommunitiesVis.getIndex()
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send(response);
                    });
            } else {
                try {
                    JobManager.createJob(0, "getFilesIndex")
                        .then(function (path) {
                            res.status(202).send(path);
                        })
                        .catch(function (error) {
                            res.status(400).send(error);
                        });

                } catch (error) {
                    console.error("CommunitiesVis.getIndex-> JobManager.createJob: error: " + error)
                }
            }
        })
        .catch(function (response) {
            console.error("CommunitiesVis.getIndex -> Flags.getFlags: error: " + response)
        });

    // CommunitiesVis.getIndex()
    //     .then(function (response) {
    //         res.status(200).send(response);
    //     })
    //     .catch(function (response) {
    //         res.status(400).send(response);
    //     });
// });
};

// router.get('/file/:fileId', function (req, res, next) {
module.exports.getFile = function getFile(req, res, next) {
    const fileId = req.params[idParam_fileId];

    Flags.getFlagById(fileId)
        .then(function (flag) {
            if (flag == null) { // flag does not exist => no update needed
                CommunitiesVis.getById(fileId)
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send(response);
                    });
            } else { //flag exist
                JobManager.createJob(fileId, "getFileById")
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
        })
        .catch(function (response) {
            res.status(400).send("invalid file id");
        });

    // CommunitiesVis.getById(fileId)
    //     .then(function (response) {
    //         res.status(200).send(response);
    //     })
    //     .catch(function (response) {
    //         res.status(400).send(response);
    //     });
    // }
// });
};