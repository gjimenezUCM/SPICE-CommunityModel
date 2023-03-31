'use strict';

const idParam_jobId = 'jobId';

var express = require('express');
const {response} = require("express");

var router = express.Router();


const Job = require("./job.js");

const jobsHandler = require("./jobsHandler.js");
var jobManager = require('./jobsManager.js');


var jobPrefix = "/v2.0/jobs-manager/jobs/";


/**Response templates */
var jobStarted = {
    "job": {
        "path": "xxx",
        "jobId": "xx",
        "name": "CM Update",
        "job-state": "STARTED",
        "time-created": -1,
        "time-completed": -1,
        "time-to-autoremove-job": -1,
        "data": {}
    }
}
var jobCompleted = {
    "job": {
        "path": "",
        "jobId": "",
        "name": "CM Update",
        "job-state": "COMPLETED",
        "time-created": -1,
        "time-completed": -1,
        "time-to-autoremove-job": -1,
        "data": {}
    }
}


/**
 * Returns filled response template
 * @param {Job} job
 * @param {String} data
 * @returns Completed response
 */
function generateCompletedResponse(job, data) {
    var response = jobCompleted;
    var timeLeft = -1;
    if (job.jobState !== Job.jobStates.ERROR) {
        var msLeft = job.timeCompleted.getTime() + jobManager.timeoutAfterCompletion - (new Date().getTime());
        var dateLeft = new Date(msLeft);
        timeLeft = dateLeft.getMinutes() + ":" + dateLeft.getSeconds();
    }
    response["job"]["job-state"] = job.jobState;
    response["job"]["path"] = jobPrefix + job.jobId;
    response["job"]["jobId"] = job.jobId;
    response["job"]["data"] = data;
    response["job"]["time-created"] = job.timeCreated;
    response["job"]["time-completed"] = job.timeCompleted;
    response["job"]["time-to-autoremove-job"] = timeLeft;
    return response
}

/**
 * Returns filled response template
 * @param {Job} job
 * @returns Progress response
 */
function generateProgressResponse(job) {
    var data = {}
    var response = jobStarted;
    response["job"]["job-state"] = job.jobState;
    response["job"]["path"] = jobPrefix + job.jobId;
    response["job"]["jobId"] = job.jobId;
    response["job"]["data"] = data;
    response["job"]["time-created"] = job.timeCreated;
    response["job"]["time-completed"] = job.timeCompleted;
    return response
}


/**
 * /jobs/:job_id GET request
 * Allows to monitor job status and get data if CM update is finished.
 *
 */
// router.get('/:job_id', function (req, res, next) {
module.exports.getJob = function getJob(req, res, next) {
    const jobId = req.params[idParam_jobId]

    try {
        // console.log("List of current jobs: ");
        // console.log(JSON.stringify(jobManager.getJobs(), null, " "));

        var job = jobManager.getJob(jobId);

        if (job == null) {
            res.status(404).send("JobsManager: Job not found");
        } else {
            console.log("Monitoring Job: <" + job.jobId + ">");

            if (job.jobState === Job.jobStates.INQUEUE || job.jobState === Job.jobStates.STARTED) {
                res.send(generateProgressResponse(job));
            } else if (job.jobState === Job.jobStates.COMPLETED || job.jobState === Job.jobStates.ERROR) {
                jobsHandler.getData(job.request, job.param)
                    .then(function (data) {
                        res.status(200).send(generateCompletedResponse(job, data));
                    })
                    .catch(function (error) {
                        res.status(404).send("JobsManager: getJob.getData exception: " + error);
                    });
            }
        }
    } catch (error) {
        console.error("<JobsRoute> ERROR get: " + error);
    }
// });
};


module.exports.getJobs = function getJobs(req, res, next) {
    let jobs = jobManager.getJobs();
    let response = [];
    let error = null;

    for (let i = 0; i < jobs.length; i++) {
        // if (jobs[i].jobState === Job.jobStates.COMPLETED || jobs[i].jobState === Job.jobStates.ERROR) {
        //     jobsHandler.getData(jobs[i].request, jobs[i].param)
        //         .then(function (data) {
        //             response[i] = generateCompletedResponse(jobs[i], data);
        //         })
        //         .catch(function (err) {
        //             error = "JobsManager: getJobs.getData exception: " + err
        //         });
        // } else {
        response[i] = jobs[i];
        // }
        // if (error != null)
        //     break;
    }

    // if (error === null) {
    res.status(200).send(response);
    // } else {
    //     res.status(404).send(error);
    // }


}

// module.exports.deleteJobs = function deleteJobs(req, res, next) {
//     res.status(200).send("Work In Progress");
// }



// module.exports = router;