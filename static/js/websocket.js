(function(){

    var getWebsocketAddress = function(){
        var address = window.location.protocol === 'https:' ? 'wss://': 'ws://';
        if (window.location.port){
            address += window.location.host + '/api/ws';
        } else {
            address += window.location.host + '/api/ws';
        }
        return address;
    }
    var wsAddress = getWebsocketAddress();
    var ws = new ReconnectingWebSocket(wsAddress);

    ws.onopen = function(){
        console.log("Websocket connection established");
    }

    ws.onmessage = function(message){
        console.log("Message received: " + message.data);
    }

    ws.onclose = function(){
        console.log("Websocket connection closed");
    }

    ws.onerror = function(){
        console.log("Websocket connection error");
    }

    window.ws = ws;
})();