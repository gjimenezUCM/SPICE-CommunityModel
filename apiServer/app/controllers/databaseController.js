'use strict';
const DatabaseContrl = require('../service/databaseControllerService');

// var express = require('express');
// var router = express.Router();


/**
 http://localhost:8080/database-controller/dump

 /Get -> Returns current state of DB
 /Post w/ json -> Clears and loads data to DB

 */

// router.get('/dump', function (req, res, next) {
module.exports.getDump = function getDump(req, res, next) {
    DatabaseContrl.getDump()
        .then(function (response) {
            res.status(200).send(response);
        })
        .catch(function (response) {
            res.status(400).send(response);
        });
// });
};

// router.post('/dump', function (req, res, next) {
module.exports.postDump = function postDump(req, res, next) {
    DatabaseContrl.postLoad(req.body)
        .then(function (response) {
            res.status(200).send(response);
        })
        .catch(function (response) {
            res.status(400).send(response);
        });
// });
};


// // router.get('/reset', function (req, res, next) {
// module.exports.getReset = function getReset(req, res, next) {
//     const empty = {};
//     DatabaseContrl.postLoad(empty)
//         .then(function (response) {
//             res.status(200).send(response);
//         })
//         .catch(function (response) {
//             res.status(400).send(response);
//         });
// // });
// };


// module.exports = router;