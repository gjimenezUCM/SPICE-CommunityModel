module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      id: String,
      name: String,
      algorithm: {
        name: String,
        params: [
          String
        ],
        weight: String,
        weightArtworks: String
      },
      similarity_functions: [{
        _id: false,
        sim_function: {
          name: String,
          weight: Number,
          params: [
            {
              artworkId: String,
              att_type: String
            }
          ],
          on_attribute: {
            att_name: String,
            att_type: String
          },
          dissimilar: Boolean
        }
      }],
      user_attributes: [{
        _id: false,
        att_name: String,
        att_type: String
      }],
      interaction_similarity_functions: [{
        _id: false,
        sim_function: {
          name: String,
          params: [
            String
          ],
          on_attribute: {
            att_name: String,
            att_type: String
          },
          interaction_object: {
            att_name: String,
            att_type: String
          },
          dissimilar: Boolean
        }
      }]
    }, { minimize: false }
  );

  // PRE MIDDLEWARE
  schema.pre('save', function (next) {
    this.id = this._id;
    next();
  });

  schema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    // object.id = _id.toString();
    return object;
  });

  const Perspectives = mongoose.model("Perspectives", schema);

  // Access mongobd and retrieve requested data
  return {
    insertPerspective: function (data, onSuccess, onError) {
      // console.log(json);
      Perspectives.create(data, function (err, res) {
        if (err) {
          console.log("insertPerspective: error");
          onError(err);
        }
        else {
          // console.log(res.id.toString())
          onSuccess(res.id.toString());
        }
      });
    },
    all: function (onSuccess) {
      let items = [];
      Perspectives.find({}, { projection: { _id: 0 } }, function (error, data) {
        let i = 0;
        data.forEach(element => {
          items[i] = element.toJSON();
          i++;
        });
        onSuccess(items);
      });

    },
    getById: function (id, onSuccess, onError) {
      Perspectives.findOne({ "id": id }, { projection: { _id: 0 } }, function (error, data) {
        if (error) {
          onError(error);
        } else {
          if (data) {
            // console.log(data.toJSON());
            onSuccess(data.toJSON());
          }
          else {
            onError(id);
          }
        }
      });
    },
    allCommunitiesCreatedForPerspective: function (perspectiveId, onSuccess, onError) {
      let items = [];
      // Perspectives.find({ users: userId }, function (error, data) {
      //   if (data.length > 0) {
      //     let i = 0;
      //     data.forEach(element => {
      //       items[i] = element.toJSON();
      //       i++;
      //     });
      //     onSuccess(items);
      //   }
      //   else {
      //     onError(userId);
      //   }
      // });
    }
  };
};
