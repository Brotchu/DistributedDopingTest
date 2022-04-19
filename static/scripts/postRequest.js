let url="formtest"

function makePostRequest(urlPath, jsonDataString) {
    fetch(urlPath, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: jsonDataString
    }).then(res => {
        console.log(res)
        if(res.status==200) {
            window.location.replace("/success_page");
        }
    });
}



async function makeAthleteRegistration(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_athlete_registration');
    btnSubmit.disabled= true;
    setTimeout(()=> btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(jsonData);
    makePostRequest('register', JSON.stringify(jsonData));
}


const athleteRegistration = document.querySelector("#athleteRegistration");
if (athleteRegistration) {
    athleteRegistration.addEventListener("submit", function(e){
        makeAthleteRegistration(e, this);
    });
}

//ado

async function makeAdoRegistration(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_ado_registration');
    btnSubmit.disabled= true;
    setTimeout(()=> btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(jsonData);
    makePostRequest('register', JSON.stringify(jsonData));
}


const adoRegistration = document.querySelector("#adoRegistration");
if (adoRegistration) {
    athleteRegistration.addEventListener("submit", function(e){
        makeAdoRegistration(e, this);
    });
}
