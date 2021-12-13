// Full Documentation - https://docs.turbo360.co
const express = require('express')
const router = express.Router()

//Front page, nothing interesting here
router.get('/', (req, res) => {
  res.render('index', { text: 'This is the dynamic data. Open index.js from the routes directory to see.' })
})

//Tweet scheme and link to all tweets. 
const tweet = require("../models/tweet")
router.get("/tweets", (req, res) =>{
  tweet.find()
  .then(tweets => {
    res.json({
      confirmation: "sucess",
      data: tweets
    })
  })
  .catch(err => {
    res.json({
      cofirmation:"failure",
      data: err.message
    })
  })
})

//The landing page
router.get("/landing", (req, res) =>{
  res.render('landing', { text: "Nothing to see here" })
})

//Testing implementing style
router.get("/style", (req, res) =>{
  res.render('test-Styles', { text: "Nothing to see here" })
})

//Starting the education page
router.get("/education", (req, res) =>{
  res.render('education', { text: "Nothing to see here" })
})





//This handles the result. The search result. 
router.post("/result", (req, res) =>{
  const searchWord = req.body["term"]
  const regex = new RegExp(searchWord, "g")
  const search = tweet.find()
  const filter = { 
    Message: regex 
  }

  search.find(filter)
  .then(tweets => {
    res.json({
      data:tweets
    })
    console.log(tweets)
  })
  .catch(err => {
    res.json({
      data: "fail", 
      message: "nothing"
    })
  })
})






module.exports = router
