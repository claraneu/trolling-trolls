const express = require('express')
const router = express.Router()
const bcrypt = require("bcryptjs")
const passport = require("passport")

// Use this for debugging here
// (err, user, info)=>{
  // //console.log("Prolem solving")
  // console.log(err)
  // console.log(user)
  // console.log(info)}

// Load User model
const User = require('../models/user');
const { forwardAuthenticated } = require('../auth');
const { ensureAuthenticated } = require('../auth');

// Login Page
router.get('/login', forwardAuthenticated, (req, res) => res.render('login'));

// Register Page
router.get('/register', forwardAuthenticated, (req, res) => res.render('register'));

//Protected sample page, delete later
router.get('/dashboard', ensureAuthenticated, (req, res) =>
  res.render('dashboard', {
    user: req.user
  })
);

router.post("/login", (req, res, next)=>{
  passport.authenticate("local", {
    successRedirect: "/style",            //That must be directed to something usefull.Right now it just goes to not projected pages.  
    failureRedirect: "/users/login", 
    failureFlash: true
  })(req, res, next)
})

//Register Handle
router.post("/register", (req,res)=>{


  const { username, email, password, password2 } = req.body

  let errors = []

  if(!username || !email || !password || !password) {
    errors.push({ msg: "Please fill in all fieds!"})
  }

  if(password !== password2) {
    errors.push({ msg: "The passwords must match!"})
  }

  if(password.length < 6) {
    errors.push({ msg: "Your password should be 6 or more charakters long!"})
  }

  if(errors.length > 0) {
    // Validation not passed
    res.render("register", {
      errors,
      username,
      email,
      password,
      password2
    })
  } else {
    // Validation passed
    //Check if the user is already in the database: Find a User-scheme where 
    //the "email-column" matches the email we received just now. 
    User.findOne({ email: email})
    .then(user =>{
      if(user) {
        errors.push({ msg: "E-mail is already used. Please log in"})
        res.render("register", {
          errors,
          username,
          email,
          password,
          password2
        })
      } else {
        const newUser = new User({
          username, 
          email, 
          password
        }) 
        //Hash the password 
        bcrypt.genSalt(12, (err, salt)=>{
         bcrypt.hash(newUser.password, salt, (err, hash)=>{
           if(err) throw err
            //Set password to hashed
           newUser.password = hash
           //Save new User
           newUser.save()
            .then(user=> {
          
              req.flash("success_msg", "You are now registered!")

              res.redirect("/users/login")
            })
            .catch(err => console.log(err))
         }) 
        })
      }
    })
  }
  errors.forEach(element => {
    console.log(element)
  });
  
})

module.exports = router 