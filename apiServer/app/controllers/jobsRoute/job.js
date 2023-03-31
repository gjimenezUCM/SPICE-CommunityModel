

/**
 * 
 */
const jobPrefix = "/v2.0/jobs-manager/jobs/";

export const jobStates = {
    INQUEUE: "INQUEUE",
    STARTED: "STARTED",
    COMPLETED: "COMPLETED",
    ERROR: "ERROR"
}

export class Job {

    // path: "",
    // jobId: jobId,
    // name: "CM Update",
    // "job-state": jobStates.INQUEUE,
    // "time-created": new Date(),
    // "time-completed": new Date(),
    // "time-to-autoremove-job": "",
    // request: request,
    // param: param,
    // autoremove: false,
    // flags_id: data

    constructor(jobId, name, request, param, flags_id) {
        this.jobId = String(jobId);
        this.name = name;
        this.jobState = jobStates.INQUEUE;
        this.timeCreated = new Date();
        this.timeCompleted = -1;
        this.timeToAutoremove = -1;
        this.request = request;
        this.param = param;
        this.flags_id = flags_id;
        this.path = jobPrefix + jobId;
    }

    /**
     * Advance state of the job
     * {job-state} -> {job-state}
     * INQUEUE,    -> STARTED,
     * STARTED,    -> COMPLETED
     */
    advanceState() {
        if (this.jobState === jobStates.INQUEUE) {
            this.jobState = jobStates.STARTED;
        }
        else if (this.jobState === jobStates.STARTED) {
            this.jobState = jobStates.COMPLETED;
            this.timeCompleted = new Date();
        }
    }

    /*
    * Getters & Setters
    */

    get jobId() {
        return this._jobId;
    }
    set jobId(jobId) {
        this._jobId = String(jobId);
    }

    get name() {
        return this._name;
    }
    set name(name) {
        this._name = name;
    }

    get jobState() {
        return this._jobState;
    }
    set jobState(jobState) {
        this._jobState = jobState;
    }

    get timeCreated() {
        return this._timeCreated;
    }
    set timeCreated(timeCreated) {
        this._timeCreated = timeCreated;
    }

    get timeCompleted() {
        return this._timeCompleted;
    }
    set timeCompleted(timeCompleted) {
        this._timeCompleted = timeCompleted;
    }

    get timeToAutoremove() {
        return this._timeToAutoremove;
    }
    set timeToAutoremove(timeToAutoremove) {
        this._timeToAutoremove = timeToAutoremove;
    }

    get request() {
        return this._request;
    }
    set request(request) {
        this._request = request;
    }

    get param() {
        return this._param;
    }
    set param(param) {
        this._param = param;
    }

    get flags_id() {
        return this._flags_id;
    }
    set flags_id(flags_id) {
        this._flags_id = flags_id;
    }

    get path() {
        return this._path;
    }
    set path(path) {
        this._path = path;
    }

}
