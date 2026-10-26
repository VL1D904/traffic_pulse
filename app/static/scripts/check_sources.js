const sourcesList = document.querySelectorAll(".source");

function check_video_status() {
    sourcesList.forEach((source) => {
        let status;
        let url = `/video_api/video_status?video_id=${source.dataset.id}`
        fetch(url)
        .then((response) => {
            if (response.ok){
                return response.json()
            }
            else{
                console.log(response.json())
                throw new Error(response.status);
            }
        })
        .then((jsonData) => {
            status = jsonData["status"];
            console.log(status)
            updateStatusSpan(source, status)
        })
        .catch((error) => {
            console.log(error);
        })
    })
    setTimeout(check_video_status, 1000)
}

function updateStatusSpan(source, status){
    var videoStatusElem = source.querySelector(".videoStatus");
    var videoButton = source.querySelector("button")
    if (status === "active"){
        videoStatusElem.textContent = "Активна";
        videoStatusElem.id = "active";

        if (videoButton !== null){
            videoButton.textContent = "Остановить трансляцию"
            videoButton.id = "stopWorker"
        }
    }
    else if (status == "inactive"){
        videoStatusElem.textContent = "Отключена";
        videoStatusElem.id = "completed";
        if (videoButton !== null){
            videoButton.textContent = "Запустить трансляцию"
            videoButton.id = "startWorker"
            
        }
    }
}

check_video_status();