/***
/**

/**
 * Priorities 
 */
 //const {user_dict_radio} = require('./select.js');
//import {user_dict_radio} from 'select.js';


if(typeof document !== "undefined") { 

    const element = document.getElementById("submitAll");
    element.addEventListener("click", function() {
        var user_dict = {}

        document.getElementById("demo").innerHTML = "";
        var selected1 = document.querySelector('input[name="one"]:checked').value;
        user_dict["priority1"] = selected1; 

        var selected2 = document.querySelector('input[name="two"]:checked').value;
        user_dict["priority2"] = selected2;

        var selected3 = document.querySelector('input[name="three"]:checked').value;
        user_dict["priority3"] = selected3;


        /*** User Interests  */
        var userInterest = document.getElementById('interest_bio').value;
        console.log(userInterest);
        user_dict["userBio"] = userInterest;

        // Getting the age and borough from another js
        //console.log(user_dict_radio.Boroughs);

        //EXPORTING USER DATA
        //module.exports = {user_dict}
        

        console.log(user_dict);
    });

    
    
    /**
     * Parse to  JSON String 
    
    const spawner = require('child_process').spawn;


    /*const userinfo = {
        data_send: 'send this to python script',
        data_returned: undefined
    };


    console.log('Data sent to python script:', user_dict);

    const python_process = spawner('python', ['./test2.py', JSON.stringify(user_dict)]);

    python_process.stdout.on('data', (data) => {
        console.log('Data received form python script:', JSON.parse(data.toString()))
    });
    */


    // ...
    
    var request = require('request-promise');
  
    async function get_data() {
  
    // This variable contains the data
    // you want to send 
        var data = {
            user_dict
        }
  
        var options = {
            method: 'POST',
  
            // http:flaskserverurl:port/route
            uri: 'http://127.0.0.1:5000/get_data',
            body: data,
  
            // Automatically stringifies
            // the body to JSON 
            json: true
        };
  
        var sendrequest = await request(options)
  
        // The parsedBody contains the data
        // sent back from the Flask server 
        .then(function (parsedBody) {
            console.log(parsedBody);
              
            // You can do something with
            // returned data
            let recommendations;
            recommendations = parsedBody['recommendations'];
            console.log("Recommendations : ", recommendations);
        })
        .catch(function (err) {
            console.log(err);
        });
    }
  
    get_data();

}

else {
    console.log('nothing')
}


