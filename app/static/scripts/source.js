const adminButton = document.querySelector(".adminButton");


adminButton.addEventListener("click", () => {
    if (adminButton.id === null){
        return;
    }
    else if (adminButton.id === "startWorker"){
        var url = "/start_worker";
        var method = "PUT";
    }
    else if (adminButton.id === "stopWorker"){
        var url = "/stop_worker";
        var method = "DELETE";
    }

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: JSON.stringify({"video_id": adminButton.dataset.id})
    });
})