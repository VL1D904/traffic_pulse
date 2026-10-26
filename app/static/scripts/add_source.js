const addButton = document.getElementById("addSourceButton");
const sourceWindow = document.getElementById("addSourceWindow");
const overlay = document.getElementById("overlay");
const closeButton = document.getElementById("close");
const addSource = document.getElementById("addButton");
const errorMessage = document.getElementById("error");


addButton.addEventListener("click", () => {
    overlay.style.display = "block";
    sourceWindow.style.display = "block";
})

closeButton.addEventListener("click", () => {
    overlay.style.display = "none";
    sourceWindow.style.display = "none";
})

addSource.addEventListener("click", () => {
    var url = document.getElementById("url").value;
    var city = document.getElementById("city").value;
    var street = document.getElementById("street").value

    if (url.trim().length && city.trim().length && street.trim().length){
        var sourceData = {
            "url": url,
            "city": city,
            "street": street
        }

        fetch("/video_api/add_source", {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify(sourceData)
        })
        .then((response) => {
            return response.json();
        })
        .then((jsonData) => {
            alert(jsonData['message']);
            window.location.reload();
        })
        document.getElementById("url").value = "";
        document.getElementById("city").value = "";
        document.getElementById("street").value = "";
    }
    else{
        errorMessage.style.display = 'block';
    }
})