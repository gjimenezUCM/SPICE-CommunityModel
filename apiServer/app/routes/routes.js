// Adds rest actions defined in openapi.yaml and jobs managet to the router
const basicAuth = require("./helpers/basic-auth.js");

const swaggerUI = require("../api/swagger-ui-express");
const YAML = require('yaml')
const yaml = require('js-yaml');
const fs = require('fs');

module.exports = app => {


    const customControllers = {
        Communities: require("../controllers/communities.js"),
        Similarity: require("../controllers/similarity.js"),
        Users: require("../controllers/users.js"),
        Perspectives: require("../controllers/perspectives.js"),
        Visir: require("../controllers/visir.js"),
        Logs: require("../controllers/logs.js"),
        DatabaseController: require("../controllers/databaseController.js"),
        JobsRouter: require("../controllers/jobsRoute/jobsRoute.js")
    };

    function initRouters(router) {
        try {
            const doc = yaml.load(fs.readFileSync(app.get("apiSpec"), 'utf8'));
            router.path = doc.servers[0].url;
            let routes = [];
            for (let path in doc.paths) {
                let newPath = transformPath(path);
                const restActions = ['get', 'post', 'put', 'delete'];
                for (const action of restActions) {
                    if (doc.paths[path][action]) {
                        if (doc.paths[path][action]['operationId'] != "none") {
                            let service = doc.paths[path][action]['x-swagger-router-controller'];
                            let method = doc.paths[path][action]['operationId'];
                            router[action](newPath, customControllers[service][method]);
                        }
                    }
                }
            }
        } catch (e) {
            console.log(e);
        }
    }

    function transformPath(path) {
        const regex = /{([^}]+)}/g;
        let parameters = path.match(regex);
        let result = path;
        if (parameters) {

            for (let i = 0; i < parameters.length; ++i) {
                let word = parameters[i].slice(1, -1);
                let words = word.split('-');
                for (let j = 1; j < words.length; ++j) {
                    let temp = words[j];
                    words[j] = temp.charAt(0).toUpperCase() + temp.slice(1);
                }
                parameters[i] = ":" + words.join('');
            }
            result = path.replace(regex, () => parameters.shift());
        }
        return result;
    }

    const express = require("express");

    var router = express.Router();



    // interactive API
    const file = fs.readFileSync(app.get("apiSpec"), 'utf8')
    const swaggerDocument = YAML.parse(file)


    // var options = {
    //     customCss: '.swagger-ui .topbar { display: none }',
    //     customSiteTitle: "New Title",
    //     customfavIcon: __dirname+"/api/img/favicon.png",
    //     explorer: true
    // };

    var options = {
        customSiteTitle: "SPICE Community Model - Interactive API",
        customfavIcon: "./api/img/favicon.png",
        customCss: `
        .swagger-ui .topbar { display: none }
        .topbar-wrapper img {
            content: url("./api/img/favicon.png");
            max-width : 90px ;
        }
        .topbar-wrapper {
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }

        .topbar-wrapper a {
            max-width: 90px ;
        }

        .topbar {        
            padding: 15px 0 !important;
            background: red ;
        }
        
        .spice {
            width: 100%;
            background-color: #E4D7C8;
            padding: 3.5em;
        }
        .spice h1 {
            color: #935D55;
        }
        .spice a {
            color: #F57D0B;
            text-decoration: none;
        }
    `

    };

    app.use(
        '/api-docs',
        express.static("./api/swagger-ui-dist/", {index: false}),
        swaggerUI.serve,
        swaggerUI.setup(swaggerDocument, options)
    );

    // To use auth add basicAuth before initRouters()
    // app.use('/v2.0/visir', basicAuth);
    // app.use('/v2.0/databaseController', basicAuth);
    // app.use('/v2.0/logs', basicAuth);
    // app.use('/v2.0/jobs', basicAuth);

    app.use('/v2.0', basicAuth);

    initRouters(router);
    app.use('/', express.static('api'));
    app.use(router.path, router);

};