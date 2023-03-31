module.exports = basicAuth;


function basicAuth(req, res, next) {


    // check for basic auth header
    if (!req.headers.authorization || req.headers.authorization.indexOf('Basic ') === -1) {
        return res.status(401).json({message: 'Missing Authorization Header'});

    }
    // verify auth credentials
    const base64Credentials = req.headers.authorization.split(' ')[1];
    const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii');
    const [username, password] = credentials.split(':');
    // const user = await userService.authenticate({ username, password });

    const user = process.env.API_USER;
    const pass = process.env.API_PASS;

    // console.log("Received auth headers: " + req.headers.authorization + " -> " + username + " " + password)
    // console.log("Current user-pass: " + user + " " + pass)

    const valid = (username == user) && (password == pass)

    if (!valid) {
        return res.status(401).json({message: 'Invalid Authentication Credentials'});
    }

    // attach user to request object
    // req.user = user

    next();
}