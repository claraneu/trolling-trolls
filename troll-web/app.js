// Full Documentation - https://docs.turbo360.co
//const vertex = require('vertex360')({ site_id: process.env.TURBO_APP_ID })
const express = require('express')
var mongoose = require("mongoose")
const path = require('path')
const hogan = require("hogan-middleware")
const flash= require("connect-flash")
const session= require("express-session")
const passport = require("passport")
var dbURL = require("./properties").DB_URL

// initialize app. It defines the views(dynamic html-like files), view-engine(what framework is used for dynamic files)
//and the hogan express what I would have to research still
const app = express()
app.set("views", path.join(__dirname, "views"))
app.set("view engine", "mustache")
app.engine("mustache", hogan.__express)

//Declare public folder as the directory for static assets
app.use(express.static(path.join(__dirname, "public")))

// The mongose Way (use if turbo fails you!!)
mongoose.connect(dbURL)
mongoose.connection.on("connected", ()=>{
  console.log("connected to MongoDB using Moongoose")
})




//Passport middelware
require("./passport")(passport)


//Fix this before going into production!
//Warning The default server-side session storage, MemoryStore, is purposely not designed for a production environment. It will leak memory under most conditions, does not scale past a single process, and is meant for debugging and developing.
//Express Session middleware
app.use(session({
  secret: 'keyboard',
  resave: true,
  saveUninitialized: true,

}))



//These two are lines allow to read the body of a request. For example that is typed into a form
//formerly done by body-parser. 
app.use(express.json())
app.use(express.urlencoded({ extended: false }))


//Fix this before going into production!
//Warning The default server-side session storage, MemoryStore, is purposely not designed for a production environment. It will leak memory under most conditions, does not scale past a single process, and is meant for debugging and developing.
//Express Session middleware
app.use(session({
  secret: 'secret',
  resave: true,
  saveUninitialized: true,
}))



//Flash allows to send messages that come from one page to the next
app.use(flash())

// Passport middleware
app.use(passport.initialize());
app.use(passport.session());

// Doesnt work
//Global variables created in a peace of costum middelware. 
app.use((req, res, next)=>{
  res.locals.success_msg = req.flash("success_msg") //works
  res.locals.error_msg = req.flash("error_msg")     //not tested yet!#needs restricted resourse!!
  res.locals.error = req.flash("error")             //works
  next()
})


// localhost port
app.listen(3000)












// import routes
const index = require("./routes/index") //For pages that do not require log-in
const users = require("./routes/users") //For pages that require log-in
// set routes
app.use("/", index) //For pages that do not require log-in
app.use("/users", users) // For pages that require log-in 

module.exports = app

