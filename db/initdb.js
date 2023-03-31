let spiceUser = _getEnv('MONGODB_USER');
let spicePwd = _getEnv('MONGODB_PASSWORD');
let dbName = _getEnv('MONGO_INITDB_DATABASE');
db = new Mongo().getDB(dbName);
print("Connected to " + db.getName());

db.createUser({
  user: spiceUser,
  pwd: spicePwd,
  roles: [
    {
      role: 'readWrite',
      db: db.getName()
    }
  ]
});

db.createCollection('users', { capped: false });
db.users.deleteMany({});

db.createCollection('perspectives', { capped: false });
db.perspectives.deleteMany({});

db.createCollection('communitiesVisualization', { capped: false });
db.communitiesVisualization.deleteMany({});

db.createCollection('communities', { capped: false });
db.communities.deleteMany({});

db.createCollection('similarities', { capped: false });
db.similarities.deleteMany({});

db.createCollection('flags', { capped: false });
db.flags.deleteMany({});

db.createCollection('distanceMatrixes', { capped: false });
db.distanceMatrixes.deleteMany({});

db.createCollection('artworkDistanceMatrixes', { capped: false });
db.artworkDistanceMatrixes.deleteMany({});

db.createCollection('interactionDistances', { capped: false });
db.interactionDistances.deleteMany({});


