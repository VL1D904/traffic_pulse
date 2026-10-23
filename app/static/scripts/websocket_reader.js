const sourcesList2 = document.querySelectorAll(".source");


class WebsocketReader{
    constructor(url){
        this.url = url;
        this.socket = null;
    }

    connect(videoElem) {
        this.socket = new WebSocket(this.url);

        this.socket.onmessage = (event) => {
            let base64Data = event.data;
            let imageSrc = `data:/image/jpg;base64,${base64Data}`;
            videoElem.src = imageSrc;
        }

        this.socket.onclose = (event) => {
            this.close();
        }
    }

    close() {
        if (this.socket){
            this.socket.close()
        }
    }
}

function startWebsocket() {
    sourcesList2.forEach((source) => {
        let url = `ws://127.0.0.1:8000/ws/get_plot/${source.id}`
        const websocket_reader = new WebsocketReader(url)
        var video = source.querySelector("img");
        websocket_reader.connect(video);
    });
}


startWebsocket();