const dbConfig = require("../config/db.config.js");

const mongoose = require("mongoose");

const db = {};
db.mongoose = mongoose;
db.url = dbConfig.url;
db.communityDAO = require("./community.model.js")(mongoose);
db.CommunitiesVisualizationDAO = require("./communitiesVisualization.model")(mongoose);
db.similarityDAO = require("./similarity.model.js")(mongoose);
db.usersDAO = require("./users.model.js")(mongoose);
db.perspectivesDAO = require("./perspective.model.js")(mongoose);
db.flagDAO = require("./flag.model.js")(mongoose);
db.logsDAO = require("./logs.model.js")(mongoose);

// Connects to mongoDB
module.exports = {
    init: async function (onReady) {
        console.log(db.url);
        db.mongoose
            .connect(db.url, {
                useNewUrlParser: true,
                useUnifiedTopology: true
            })
            .then(() => {
                console.log("Connected to the database!");
                onReady();
            })
            .catch(err => {
                console.log("Cannot connect to the database!", err);
                process.exit();
            });
    },
    communities: db.communityDAO,
    communitiesVisualization: db.CommunitiesVisualizationDAO,
    similarities: db.similarityDAO,
    users: db.usersDAO,
    perspectives: db.perspectivesDAO,
    flag: db.flagDAO,
    logs: db.logsDAO
};
