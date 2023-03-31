
/**
 * Sends a POST request to api_loader.py to update CM clustering 
 */


const axios = require('axios');

const { resolve } = require('path');

module.exports.postData  = function postData(body, path)  {
    var data = JSON.stringify(body)

    let port = process.env.CM_DOCKER_PORT || 8090;
    let url = "http://cm:" + port + path;

    return new Promise((resolve, reject) => {
        try {

            axios.post(url, data)
                .then((response) => {
                    // console.log("data: "+ response.data);
                    // console.log("status: " + response.status);
                    // console.log("statusText: "+ response.statusText);
                    resolve(body);
                })
                .catch((error) => {
                    console.log("postData.Promise.axios.post: " + error)
                    reject("postData.Promise.axios.post: " + error);
                });


        } catch (error) {
            console.log("postData.Promise.axios:" + error)
            reject("postData.Promise.axios:" + error);
        }
    })
};

module.exports.getData  = function getData(path)  {
    let port = process.env.CM_DOCKER_PORT || 8090;
    let url = "http://cm:" + port + path;

    return new Promise((resolve, reject) => {
        try {

            axios.get(url)
                .then((response) => {
                    // console.log("data: "+ response.data);
                    // console.log("status: " + response.status);
                    // console.log("statusText: "+ response.statusText);
                    resolve(response.data);
                })
                .catch((error) => {
                    console.log("getData.Promise.axios.get: " + error)
                    reject("getData.Promise.axios.get: " + error);
                });


        } catch (error) {
            console.log("getData.Promise.axios:" + error)
            reject("getData.Promise.axios:" + error);
        }
    })
};