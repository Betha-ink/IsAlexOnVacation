const url = "/api/vacation"

checkState();
setCurrentDate();

function checkState() {
    fetch(url)
        .then((response) => {

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            return response.json();
        })
        .then((data) => {
            changeStateText(data["onVacation"])
        })
        .catch((error) => {
            console.log(`Could not fetch status: ${error}`);
            changeStateText(null)
        });
}

function changeStateText(state) {
    const statusElement = document.getElementById("statusBox");
    const infoElement = document.getElementById("infoText");

    switch (state) {
        case true:
            statusElement.innerHTML = "Yes.";
            infoElement.innerText = "Alex is currently on vacation. Please try reaching him again in a couple of days."
            break;
        case false:
            statusElement.innerHTML = "No.";
            infoElement.innerText = "Alex is currently working to put bread on the table for his wives and children."
            break;
        default:
            statusElement.innerHTML = "Unknown.";
            infoElement.innerText = "Alex's current whereabouts are unknown. He could be anywhere, even behind you."
    }

}

function setCurrentDate() {
    const date = new Date();

    const YYYY = date.getFullYear();
    let MM = date.getMonth() + 1; // Months start at 0!
    let DD = date.getDate();
    let hh = date.getHours();
    let mm = date.getMinutes();

    if (DD < 10) DD = '0' + DD;
    if (MM < 10) MM = '0' + MM;
    if (hh < 10) hh = '0' + hh;
    if (mm < 10) mm = '0' + mm;

    const dateString = DD + '.' + MM + '.' + YYYY + ' ' + hh + ':' + mm;

    const stateElement = document.getElementById("dateText");

    stateElement.innerText = "Last checked: " + dateString;
}


