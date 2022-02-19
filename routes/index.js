// Full Documentation - https://docs.turbo360.co
const express = require('express')
const router = express.Router()

const spawn = require('child_process').spawn;

//The landing page
router.get("/search", (req, res) =>{
  res.render('search', { text: "Nothing to see here" })
})

//Testing implementing style
router.get("/style", (req, res) =>{
  res.render('test-Styles', { text: "Nothing to see here" })
})

//Starting the education page
router.get("/education", (req, res) =>{
  res.render('education', { text: "Nothing to see here" })
})

//Starting the education page
router.get("/about", (req, res) =>{
  res.render('about', { text: "Nothing to see here" })
})

//Front page, nothing interesting here
router.get('/', (req, res) => {
  res.render('test-Styles')
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


router.post("/result", (req, res) =>{
  const searchWord = req.body["term"]
  const pyInput = {"input": searchWord}
  const pathToPyScript = "C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional zero-shot\\Scripts\\python.exe"
  //-m venv C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional^ zero-shot\\Scripts\\python.exe && python


  const pythonProcess = spawn("C:\\Users\\n2o_j\\Documents\\Projects\\Programing\\Python\\Projects\\Functional-zero-shot\\Scripts\\python", ["prototype.py", searchWord])

  var hatespeechValues = []
  pythonProcess.stdout.on("data", (dataFromPy) => {
  
    
    dataFromPy = dataFromPy.toString()
    
    console.log(dataFromPy)
    
    //WORST REGULAR EXPRESSION EVER.it Means: seararch for racist, then some white spaces until you find a number. 
    //And the match method works in a way that whatever is in () can be addressed in [1]
    let racist = dataFromPy.match(/racist\D*(\d+)/)[1]
    let sexist = dataFromPy.match(/sexist\D*(\d+)/)[1]
    let hatespeech = dataFromPy.match(/hatespeech\D*(\d+)/)[1]
    let neutral = dataFromPy.match(/neutral\D*(\d+)/)[1]
    let negative = dataFromPy.match(/negative\D*(\d+)/)[1]
    let positive = dataFromPy.match(/positive\D*(\d+)/)[1]
    let unsure = dataFromPy.match(/unsure\D*(\d+)/)[1]


    console.log(racist, sexist, hatespeech, neutral, negative, positive, unsure)
    hatespeechValues= [racist, sexist, hatespeech, neutral, negative, positive, unsure]
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
    //Needs to sendback error statment! 
    console.log("Failed to reach python. Error: " + err);
  })
  pythonProcess.on('close', (code) => {
    console.log("closed with code " + code);
  })

  })

module.exports = router
