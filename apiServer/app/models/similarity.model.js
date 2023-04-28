module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      "target-community-id": String,
      "other-community-id": String,
      "similarity-function": String,
      value: Number
    }
  );

  schema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    return object;
  });

  const Similarity = mongoose.model("Similarities", schema);

  // Access mongobd and retrieve requested data
  return {
    allForId: function (communityId, onSuccess, onError) {
      Similarity.find({ "target-community-id": communityId }, function (error, data) {
        if (error) {
          onError(error);
        }
        else if(data.length === 0) {
          onError("empty");
        }
        else {
          let items = [];
          let i = 0;
          data.forEach(element => {
            items[i] = element.toJSON();
            i++;
          });
          onSuccess(items);
        }
      }).sort({ value: -1 });

    },
    getByIds: function (targetCommunityId, otherCommunityId, onSuccess, onError) {
      Similarity.find({ "target-community-id": targetCommunityId, "other-community-id": otherCommunityId }, function (error, data) {
        if (error || data.length === 0) {
          onError(error);
        } else {
          onSuccess(data[0].toJSON());
        }
      });
    }
  };
};

// Example por saving a similarity document in the database
// const example = new Similarity({
//   "target-community-id": "621e53cf0aa6aa7517c2afdd",
//   "other-community-id": "721e53cf0aa6aa7517c2afdd",
//   "similarity-function": "cosine",
//   value: 0.893
// });
// example.save();
