module.exports = mongoose => {
    var schema = mongoose.Schema(
        {
            id: String,
            name: String,
            perspectiveId: String,
            communities: [{
                _id: false,
                "id": String,
                "name": String,
                "explanations": [{
                    _id: false,
                    "explanation_type": String,
                    "explanation_data": { type: mongoose.Mixed, default: {} },
                    "visible": Boolean
                }],
                "users": [String]
            }],
            users: [{
                _id: false,
                "id": String,
                "label": String,
                "explicit_community": mongoose.Mixed,
                "group": Number,
                "interactions": [
                    {
                        _id: false,
                        "artwork_id": String,
                        "feelings": String,
                        "extracted_emotions": mongoose.Mixed
                    }
                ]
            }],
            similarity: [{
                _id: false,
                "u1": String,
                "u2": String,
                "value": Number
            }],
            artworks: [
                {
                    _id: false,
                    "id": String,
                    "tittle": String,
                    "author": String,
                    "year": String,
                    "image": String
                }
            ]
        }, { minimize: false }
    );

    schema.method("toJSON", function () {
        const { __v, _id, ...object } = this.toObject();
        object.id = _id.toString();
        return object;
    });

    /**
     * http://localhost:8080/visualizationAPI/file/{fileId}
     */

    const CommunitiesVis = mongoose.model("communitiesVisualization", schema, "communitiesVisualization");

    // Access mongobd and retrieve requested data
    return {
        getIndex: function (onSuccess, onError) {
            let items = [];
            CommunitiesVis.find({}, { perspectiveId: 1, name: 1 }, function (error, data) {
                let i = 0;
                data.forEach(element => {
                    let e = element.toJSON();
                    e.id = e.perspectiveId
                    delete e.perspectiveId
                    items[i] = e;
                    i++;
                });
                onSuccess(items);
            });
        },
        getById: function (id, onSuccess, onError) {
            CommunitiesVis.findOne({ perspectiveId: id }, { projection: { _id: 0 } }, function (error, data) {
                // CommunitiesVis.findOne({ perspectiveId: id }, {}, function (error, data) {
                if (error) {
                    onError(error);
                } else {
                    if (data) {
                        onSuccess(data.toJSON());
                    }
                    else {
                        onError("file with that id does not exist");
                    }
                }
            });
        }
    };
};
