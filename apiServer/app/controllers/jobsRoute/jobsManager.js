/**
 * Jobs queue manager.
 * Contains a list with jobs, and basic CRUD operations. Used to add, remove and read for specific job
 */

const Job = require("./job.js");
const Flags = require('../../service/flagsService.js');
const redirect = require('../../service/helpers/redirectRequest.js');


var jobsList = []


// time: minutes*60*1000=ms
export var timeoutAfterCompletion = 30 * 60 * 1000;

/**
 * Main loop. Executes every 2 seconds
 */
export function startJobManager() {
    // repeat 
    try {
        setInterval(function () {
            checkAndStartNewJob();
            autoremoveJobs();
        }, 2000);
    } catch (error) {
        console.error(error)
    }
};


/**
 * Set job to error state and remove the flag with error from mongoDB
 * @param {JSON} flag flag that contains the error
 * @param {String} errorMsg error message
 */
function setJobToErrorState(flag, errorMsg) {
    // create copy of the flag and preprocess the flag before comparing 
    var flagWithError = JSON.parse(JSON.stringify(flag["_id"]));

    // // find the failed job and set the state to ERROR. remove flag that contains the error
    // jobsList.forEach(elem => {
    //     elem.flags_id.forEach(elemFlag => {
    //         if ((JSON.stringify(elemFlag) == JSON.stringify(flagWithError))) {
    //             elem.jobState = Job.jobStates.ERROR;
    //             elem.request = "error";
    //             elem.param = errorMsg;
    //             elem.timeCompleted = new Date();
    //             Flags.removeFlag(flag["_id"]);
    //         }
    //     })
    // });

    //the job with error it is the current job
    var jobWithError = jobsList.find(job => (job.jobState == Job.jobStates.STARTED));
    jobWithError.flags_id.forEach(elemFlag => {
                if ((JSON.stringify(elemFlag) == JSON.stringify(flagWithError))) {
                    jobWithError.jobState = Job.jobStates.ERROR;
                    jobWithError.request = "error";
                    jobWithError.param = errorMsg;
                    jobWithError.timeCompleted = new Date();
                    Flags.removeFlag(flag["_id"]);
                }
            })
}

/**
 * Check flags and if CM is not updating then find the first job in the queue. Update CM with that job and advance the state of the job.
 */
function checkAndStartNewJob() {
    return new Promise(function (resolve, reject) {
        var cmState = "idle";

        // Check flags
        Flags.getFlags("withErrors")
            .then(function (flags) {
                if (flags == null) {
                    flags = []
                }

                // Iterate flags, check if CM is updating and if there are flags with errors
                flags.forEach(flag => {
                    //check for jobs with errors
                    if (flag["error"] !== "N/D") {
                        var errorMsg = flag["error"];
                        setJobToErrorState(flag, errorMsg)
                    }

                    if (!flag["needToProcess"] && flag["error"] == "N/D")
                        cmState = "updating";

                });

                // check for finished jobs. checking for flags from certain jobs in mongodb  
                jobsList.forEach(job => {
                    if (job.jobState == Job.jobStates.STARTED) {
                        var finished = true;
                        for (let jobflag of job.flags_id) {
                            for (let flag of flags) {
                                // compare if mongoDB has the same flags as the job
                                if (JSON.stringify(jobflag) == JSON.stringify(flag["_id"])) {
                                    finished = false;
                                }
                                if (!finished)
                                    break;
                            }
                            if (!finished)
                                break;
                        }
                        if (finished) {
                            job.advanceState();
                        }
                    }
                });


                // Find first job that need an update
                var jobToUpdate = jobsList.find(job => (job.jobState == Job.jobStates.INQUEUE));

                // If cm is not updating and there are jobs to update, then update cm and advance that job state from queue to started
                if (cmState == "idle" && jobToUpdate !== undefined) {
                    redirect.postData(jobToUpdate.param, "/update_CM")
                    jobToUpdate.advanceState();
                }

                // console.log("CM State: " + cmState);
                resolve();
            })
            .catch(function (error) {
                console.log("<JobsQueue> ERROR checkAndStartNewJobs: " + error);
                reject(error);
            });
    });
};

/**
 * Checks if there are any jobs to remove and removes them
 */
function autoremoveJobs() {
    // for in jobs
    // if actualtime > timeCompleted+livetime => then remove job
    var actualTime = new Date().getTime();
    jobsList.forEach(job => {
        if (job.jobState == Job.jobStates.COMPLETED || job.jobState == Job.jobStates.ERROR) {
            var timeRemove = job.timeCompleted.getTime() + timeoutAfterCompletion;
            if (actualTime > timeRemove) {
                removeJob(job.jobId);
            }
        }
    });
}


/**
 * Returns a path for an existing or a new job.
 * @param {string} param param (if no params then set it to integer zero '0')
 * @param {string} requestTypeName request type (getCommunities, getPerspectiveById, etc)
 * @returns jobPath
 */
export function createJob(param, requestTypeName) {
    return new Promise(function (resolve, reject) {
        findExistingJob(param, requestTypeName)
            .then(function (existingJob) {
                if (existingJob == null) {
                    var jobId = generateId()
                    console.log("<JobsQueue> Created new job")
                    console.log("<JobsQueue> GeneratedId: " + jobId)
                    console.log("<JobsQueue> Param: " + param)

                    // Add job to jobList
                    Flags.getFlags()
                        .then(function (flags) {
                            var job;
                            var name = "CM Update";
                            var flags_id = flags.map(a => a._id);
                            job = new Job.Job(jobId, name, requestTypeName, param, flags_id)
                            jobsList.push(job);
                            var data = {
                                "path": job.path
                            }
                            resolve(data);
                        })
                        .catch(function (error) {
                            console.log("<JobsQueue> ERROR createJob.Flags.getFlags: " + error)
                        });
                } else {
                    var data = {
                        "path": existingJob.path
                    }
                    resolve(data);
                }
            })
            .catch(function (error) {
                console.log("<JobsQueue> ERROR createJob.findExistingJob.promise: " + error);
                reject(error);
            });
    });
}

/**
 * Checks if a job with same parameters and request type already exist
 * Compares request, param and flags_id (without "needToProcess" field)
 * @param {string} param param
 * @param {string} requestTypeName request type
 * @returns promise that resolves with existing job or null if does not exist
 */
function findExistingJob(param, requestTypeName) {
    return new Promise(function (resolve, reject) {
        Flags.getFlags()
            .then(function (flags) {
                var job = null;
                // remove needToProcess field to compare even if the job has started

                let flags_id = flags.map(a => a._id);

                jobsList.forEach(elem => {
                    if (elem.request == requestTypeName && elem.param == param) {
                        if (JSON.stringify(elem.flags_id) == JSON.stringify(flags_id)) {
                            job = elem;
                        }
                    }
                });
                resolve(job);
            })
            .catch(function (error) {
                console.log("<JobsQueue> ERROR findExistingJob.Flags.getFlags: " + error);
                reject(error);
            });
    });
}

/**
 * Returns requested job by id
 * @param {String} jobId job Id
 * @returns job object
 */
export function getJob(jobId) {
    return jobsList.find(elem => elem.jobId === String(jobId));
}

/**
 * Returns jobs
 * @returns List with all jobs
 */
export function getJobs() {
    return jobsList;
}

/**
 * Removes job by id
 */
function removeJob(jobId) {
    var job = jobsList.find(elem => elem.jobId === String(jobId));
    if (job !== undefined) { //if still not removed by timeout
        console.log("<JobsQueue> removing job => jobId: " + jobId);
        const index = jobsList.indexOf(job);
        if (index > -1) { // only splice array when item is found
            jobsList.splice(index, 1); // 2nd parameter means remove one item only
        }
    }
}


/**
 * Generates non-repeating random 4-digit job id
 * @returns {Integer} id
 */
function generateId(jobId) {
    let id = 0;
    var ok = false;
    while (!ok) {
        id = Math.floor(
            Math.random() * (9999 - 1000) + 1000
        );
        if (jobsList.find(elem => elem.jobId === String(id)) == null)
            ok = true;
    }
    return id;
}





