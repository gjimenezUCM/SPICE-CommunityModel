module.exports = mongoose => {
    var schema = mongoose.Schema(
        {
            "_id": {
                "$oid": {
                    "type": "ObjectId"
                }
            },
            "name": {
                "type": "String"
            },
            "msg": {
                "type": "String"
            },
            "args": {
                "type": "Array"
            },
            "levelname": {
                "type": "String"
            },
            "levelno": {
                "type": "Number"
            },
            "pathname": {
                "type": "String"
            },
            "filename": {
                "type": "String"
            },
            "module": {
                "type": "String"
            },
            "exc_info": {
                "type": "Mixed"
            },
            "exc_text": {
                "type": "Mixed"
            },
            "stack_info": {
                "type": "Mixed"
            },
            "lineno": {
                "type": "Number"
            },
            "funcName": {
                "type": "String"
            },
            "created": {
                "type": "Number"
            },
            "msecs": {
                "type": "Number"
            },
            "relativeCreated": {
                "type": "Number"
            },
            "thread": {
                "$numberLong": {
                    "type": "String"
                }
            },
            "threadName": {
                "type": "String"
            },
            "processName": {
                "type": "String"
            },
            "process": {
                "type": "Number"
            },
            "username": {
                "type": "String"
            },
            "time": {
                "$date": {
                    "$numberLong": {
                        "type": "String"
                    }
                }
            },
            "host": {
                "type": "String"
            },
            "message": {
                "type": "String"
            }
        }
    );

    schema.method("toJSON", function () {
        const {__v, _id, ...object} = this.toObject();
        // object.id = _id.toString();
        return object;
    });

    const Logs = mongoose.model("log_cm", schema, "log_cm");

    // Access mongobd and retrieve requested flag
    return {
        allLogs: function (logsType, onSuccess, onError) {
            let items = [];
            if (logsType === "ALL") {
                Logs.find({}, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1});
            } else {
                Logs.find({"levelname": logsType}, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1});
            }
        },

        nLatestLogs: function (n, logsType, onSuccess, onError) {
            let items = [];
            if (logsType === "ALL") {
                Logs.find({}, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1}).limit(n);
            } else {
                Logs.find({"levelname": logsType}, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1}).limit(n);
            }
        },

        logsBetweenTwoDates: function (startDate, endDate, logsType, onSuccess, onError) {
            let items = [];
            if (logsType === "ALL") {
                Logs.find({
                    "time": {
                        $gte: startDate,        //new Date(new Date(startDate).setHours(00, 00, 00)),
                        $lte: endDate            //new Date(new Date(endDate).setHours(23, 59, 59))
                    },
                }, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1});
            } else {
                Logs.find({
                    "time": {
                        $gte: startDate,        //new Date(new Date(startDate).setHours(00, 00, 00)),
                        $lte: endDate            //new Date(new Date(endDate).setHours(23, 59, 59))
                    },
                    "levelname": logsType
                }, {projection: {_id: 0}}, function (error, data) {
                    if (error) {
                        onError(error);
                    } else {
                        let i = 0;
                        data.forEach(element => {
                            items[i] = element.toJSON();
                            i++;
                        });
                        onSuccess(items);
                    }
                }).sort({_id: -1});
            }

        }
    };
};

