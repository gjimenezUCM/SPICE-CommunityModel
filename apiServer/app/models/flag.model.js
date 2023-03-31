module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      perspectiveId: String,
      userid: String,
      needToProcess: Boolean,
      error: String
    }
  );

  schema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    // object.id = _id.toString();
    return object;
  });

  const Flags = mongoose.model("Flags", schema);

  // Access mongobd and retrieve requested flag
  return {
    insertFlag: function (data, onSuccess, onError) {
      Flags.create(data, function (err, res) {
        if (err) {
          console.error("insertFlag: error");
          onError("insertFlag:" + user);
        }
        else {
          onSuccess(res._id.toString());
        }
      });
    },

    checkFlags: function (onSuccess, onError) {
      Flags.find({}, function (error, data) {
        // var res = JSON.stringify(data)
        if (error) {
          console.error("checkFlags: error");
          onError("checkFlag:" + error);
        } else {
          if (Object.keys(data).length > 0) {
            onSuccess(data);
          }
          else {
            onSuccess(null);
          }
        }
      }).lean();
    },

    checkFlagsWithoutErrors: function (onSuccess, onError) {
      Flags.find({ 'error': 'N/D' }, function (error, data) {
        if (error) {
          console.error("checkFlagsWithoutErrors: error");
          onError("checkFlagsWithoutErrors:" + error);
        } else {
          if (Object.keys(data).length > 0) {
            onSuccess(data);
          }
          else {
            onSuccess(null);
          }
        }
      }).lean();
    },

    checkFlagById: function (id, onSuccess, onError) {
      Flags.findOne({ "perspectiveId": id }, { projection: { _id: 0 } }, function (error, data) {
        if (error) {
          console.error("checkFlagById: error");
          onError("checkFlagById:" + error);
        } else {
          if (data) {
            onSuccess(data.toJSON());
          }
          else {
            onSuccess(null);
          }
        }
      });
    },

    removeFlagById: function (id, onSuccess, onError) {
      Flags.deleteOne({ "_id": id }, function (error, data) {
        if (error) {
          console.error("removeFlagById: error");
          onError("removeFlagById:" + error);
        } else {
          onSuccess(null);
        }
      });
    }
  };
};

