const idParam_nLogs = 'nLogs';
const idParam_startDate = 'startDate';
const idParam_endDate = 'endDate';
const idParam_logsType = 'logsType';
const Logs = require('../service/logsService.js');


module.exports.getNLatestLogs = function getNLatestLogs(req, res, next) {
    const nLogs = parseInt(req.query[idParam_nLogs]);
    let logsType = req.query[idParam_logsType]

    if (logsType === undefined)
        logsType = "ALL";
    else
        logsType = logsType.toUpperCase();

    if (isNaN(nLogs)) {
        res.status(400).send("Parameter 'nLogs' is NaN");
    } else if (nLogs < 0) {
        res.status(400).send("Parameter 'nLogs' is <0");
    } else if (nLogs === 0) {
        Logs.getAllLogs(logsType)
            .then(function (response) {
                res.send(response);
            })
            .catch(function (error) {
                res.status(400).send(error);
            });
    } else if (nLogs > 0) {
        Logs.getNLatestLogs(nLogs, logsType)
            .then(function (response) {
                res.send(response);
            })
            .catch(function (error) {
                res.status(400).send(error);
            });
    }
};


module.exports.getLogsBetweenTwoDates = function getLogsBetweenTwoDates(req, res, next) {
    const startDate = req.query[idParam_startDate];
    const endDate = req.query[idParam_endDate];
    let logsType = req.query[idParam_logsType]

    if (logsType === undefined)
        logsType = "ALL";
    else
        logsType = logsType.toUpperCase();

    if (isNaN(Date.parse(startDate)) || isNaN(Date.parse(endDate))) {
        res.status(400).send("Parameters are NaN");
    } else if (new Date(startDate) >= new Date(endDate)) {
        res.status(400).send("startDate is >= than endDate");
    } else {
        Logs.getLogsBetweenTwoDates(new Date(startDate), new Date(endDate), logsType)
            .then(function (response) {
                res.send(response);
            })
            .catch(function (error) {
                res.status(400).send(error);
            });
    }
};