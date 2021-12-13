// Full Documentation - https://docs.turbo360.co
const vertex = require('vertex360')({ site_id: process.env.TURBO_APP_ID })
const express = require('express')
var mongoose = require("mongoose")
const path = require('path')
const hogan = require("hogan-middleware")
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

//These two are lines allow to read the body of a request. For example that is typed into a form
//formerly done by body-parser. 
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// localhost port
app.listen(3000)

// import routes
const index = require('./routes/index')
// const api = require('./routes/api') // sample API Routes

// set routes
app.use('/', index)
// app.use('/api', api) // sample API Routes

module.exports = app

