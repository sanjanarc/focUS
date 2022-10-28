const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");

const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    //user_dict_radio["Age"] = selected.innerHTML;
    //console.log(user_dict_radio);
    optionsContainer.classList.remove("active");
  });
});


const selected2 = document.querySelector(".selected2");
const optionsContainer2 = document.querySelector(".options-container2");

const optionsList2 = document.querySelectorAll(".option2");

selected2.addEventListener("click", () => {
  optionsContainer2.classList.toggle("active");
});

optionsList2.forEach(o => {
  o.addEventListener("click", () => {
    selected2.innerHTML = o.querySelector("label").innerHTML;
    //user_dict_radio["Boroughs"] = selected2.innerHTML;
    //console.log(user_dict_radio);
    optionsContainer2.classList.remove("active");
  });
});


// const element = document.getElementById("submitAll");
//     element.addEventListener("click", function() {
//       document.getElementById("userAge").innerHTML = user_dict_radio["Age"]
//       document.getElementById("userBorough").innerHTML = user_dict_radio["Boroughs"]


//     });


//EXPORTING TO LINK_BACKEND.JS 
//module.exports = {user_dict_radio};
//const {user} = require('./module1.js');

// const element = document.getElementById("submitAll");
//     element.addEventListener("click", function() {


