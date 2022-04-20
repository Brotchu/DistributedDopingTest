let url = "formtest"

function makePostRequest(urlPath, jsonDataString, destination) {
    fetch(urlPath, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: jsonDataString
    }).then(res => {
        console.log(res)
        if (res.status == 200) {
            window.location.replace(destination);
        }
    });
}

async function makeAthleteRegistration(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_athlete_registration');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(jsonData);
    makePostRequest('register', JSON.stringify(jsonData), "/success_page");
}

//athlete

const athleteRegistration = document.querySelector("#athleteRegistration");
if (athleteRegistration) {
    athleteRegistration.addEventListener("submit", function (e) {
        makeAthleteRegistration(e, this);
    });
}


async function makeAthleteLogin(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_athlete_login');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(JSON.stringify(jsonData));
    makePostRequest('login', JSON.stringify(jsonData), "/availability_page");
}


const athleteLogin = document.querySelector("#athleteLogin");
if (athleteLogin) {
    athleteLogin.addEventListener("submit", function (e) {
        makeAthleteLogin(e, this);
    });
}


//ado

async function makeAdoRegistration(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_ado_registration');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(JSON.stringify(jsonData));
    makePostRequest('register_ado', JSON.stringify(jsonData), "/success_page");
}


const adoRegistration = document.querySelector("#adoRegistration");
if (adoRegistration) {
    adoRegistration.addEventListener("submit", function (e) {
        makeAdoRegistration(e, this);
    });
}


async function makeAdoLogin(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_ado_login');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);

    // json from form
    const jsonData = {};
    for (const pair of new FormData(form)) {
        jsonData[pair[0]] = pair[1];
    }
    console.log(JSON.stringify(jsonData));
    makePostRequest('login_ado', JSON.stringify(jsonData), "/query_page");
}


const adoLogin = document.querySelector("#adoLogin");
if (adoLogin) {
    adoLogin.addEventListener("submit", function (e) {
        makeAdoLogin(e, this);
    });
}



// availability

async function makeAvailability(e, form) {
    e.preventDefault();

    const btnSubmit = document.getElementById('submit_availability');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);

    const jsonData = {
        availability: []
    };

    const startDate = $('#startDate').val();
    const endDate = $('#endDate').val();
    const location = $('#location').val();

    for (let i = startDate; i <= endDate; i++) {
        jsonData.availability.push({
            Location: location,
            Date: String(i)
        });
    }

    makePostRequest('availability', JSON.stringify(jsonData), "/end_page");
}


const availability = document.querySelector("#availability");
if (availability) {
    availability.addEventListener("submit", function (e) {
        makeAvailability(e, this);
    });
}

// ado query
