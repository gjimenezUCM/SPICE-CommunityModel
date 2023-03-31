const Users = require('../service/usersService.js');
const userParam = 'userId';


module.exports.updateUsers = function updateUsers(req, res, next) {
  let paramUserId = req.params[userParam];
  // Check if the userid in the url and in every object in the list contained in the body are the same
  if (req.body.every((ugc) => ugc.userid === paramUserId)) {
    try {
      Users.updateUsers(req.body)
        .then(function (response) {
          res.status(204);
          res.send(); 
        })
        .catch(function (response) {
          console.log(response)
          res.status(500);
          res.send(response);
        });
    } catch (error) {
      console.error(error)
    }
  } else {
    res.status(400).send("Invalid userId: userId URL differs form the userid in the body request");
  }

};

module.exports.listUserCommunities = function listUserCommunities(req, res) {
  const userId = req.params[userParam];
  Users.listUserCommunities(userId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid user id");
    });
};
