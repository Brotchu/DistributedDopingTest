let url="formtest"

function makePostRequest(urlPath, jsonDataString) {
    fetch(url, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: jsonDataString
    }).then(res => {
        console.log(res)
    });
}


async function submitAthleteRegistration(e, form){
    e.preventDefault();

    const btnSubmit = document.getElementById('submitRegistration');
    btnSubmit.disabled= true;
    setTimeout(()=> btnSubmit.disabled = false, 2000);

    //json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(jsonData);
    makePostRequest(url, JSON.stringify(jsonData));
    //use athleteRegisterRequest
}

const registrationForm = document.querySelector("#athleteRegistration");
if (registrationForm){
    registrationForm.addEventListener("submit", function(e){
        submitAthleteRegistration(e, this);
    });
}


// var xhr = new XMLHttpRequest();
    // xhr.open("POST", url, true );
    // xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.send(JSON.stringify({
    //     name: name,
    //     email: email,
    //     password: password, 
    //     confirm_password: confirm_password,
    //     country: country,
    //     location: location
    // }));