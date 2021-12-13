const mg = require("mongoose")

const tweet = new mg.Schema({
    user : {type:String, trim:true, default:""},
    RT: {type:String, trim:true, default:""},
    Message: {type:String, trim:true, default:""}

})

module.exports = mg.model("tweet", tweet)