// Full Documentation - https://docs.turbo360.co
const express = require('express')
const router = express.Router()
//Working in progress concerning data handeling. When being used on the backend
//import test from "../public/js/vis.js"
//const test = require("../public/js/vis")
const spawn = require('child_process').spawn;

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

// //Starting the log-in page
// router.get("/log-in", (req, res) =>{
//   res.render('log-in', { text: "Nothing to see here" })
// })



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


//This handles the result that are retrieved from a database 
// router.post("/result", (req, res) =>{
//   const searchWord = req.body["term"]
//   const regex = new RegExp(searchWord, "g")
//   const search = tweet.find()
//   const filter = { 
//     Message: regex 
//   }

//   search.find(filter)
//   .then(tweets => {
//     let tweet0 = tweets
//     tweet0 = JSON.stringify(tweet0)

//     const data=({
//       dataKey: tweet0
//     })

// // !!!! I AM 100 PERCENT SURE THIS IS THE WRONG WAY TO DO that!!!
//     res.render("index", data)

//   })
  
//   .catch(err => {
//     res.json({
//       data: "fail", 
//       message: "nothing"
//     })
//     console.log(err)
//   })
// })

// import "../prototype.py"

router.post("/result", (req, res) =>{
  const searchWord = req.body["term"]
  //const pyInput = {"input": searchWord}
  //const pathToPyScript = "C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional zero-shot\\Scripts\\python.exe"
  //-m venv C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional^ zero-shot\\Scripts\\python.exe && python

  const pythonProcess = spawn("C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional-zero-shot\\Scripts\\python", ["prototype.py", searchWord])


  var hatespeechValues = []
  pythonProcess.stdout.on("data", (dataFromPy) => {
    //console.log('Pipe data from python script ...');
    dataFromPy = dataFromPy.toString()
    
    console.log(dataFromPy)
    
    //WORST REGULAR EXPRESSION EVER.it Means: seararch for racist, then some white spaces until you find a number. 
    //And the match method works in a way that whatever is in () can be addressed in [1]
    let racist = dataFromPy.match(/racist.*(\d){1,4}/)[1]
    let sexist = dataFromPy.match(/sexist.*(\d){1,4}/)[1]
    let hatespeech = dataFromPy.match(/hatespeech.*(\d){1,4}/)[1]
    let neutral = dataFromPy.match(/neutral.*(\d){1,4}/)[1]
    let negative = dataFromPy.match(/negative.*(\d){1,4}/)[1]
    let positive = dataFromPy.match(/positive.*(\d){1,4}/)[1]
    console.log(racist, sexist, hatespeech, neutral, negative, positive)
    hatespeechValues= [racist, sexist, hatespeech, neutral, negative, positive]
    //return hatespeechValues
    

    var dataCompact = {
      hatespeechPred: hatespeechValues
    }
   
    dataCompact = JSON.stringify(dataCompact)
  
    const dataSendBack = {
      dataKey: dataCompact
    }
  
    res.render("index", dataSendBack)



  })

  pythonProcess.on('error', (err) => {
    console.log("Failed to reach python. Error: " + err);
  })
  pythonProcess.on('close', (code) => {
    console.log("closed with code " + code);
  })



  //     const data=({
  //       dataKey: tweet0
  //     })
  
  // // !!!! I AM 100 PERCENT SURE THIS IS THE WRONG WAY TO DO that!!!
  //     res.render("index", data)
  
  //   })


  })

module.exports = router
