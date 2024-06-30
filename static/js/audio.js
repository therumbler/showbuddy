(function(){
    let audioEl = document.getElementById('audioElement');
    let audioStream;
    let audioRecorder;
    let recordedChunks = [];

    async function stopRecording(){
        await audioRecorder.stop();
        let track = audioStream.getTracks()[0];
        await track.stop()        
    }
    async function uploadAudio(audio){
        const formData = new FormData();
        formData.append('audio', audio, 'audio.webm');
        let resp = await fetch('/api/audio', {
            method: 'POST',
            body: formData
        });
        if(!resp.ok){
            logToConsole('Error processing audio');
            return;
        }
        let data = await resp.json();
        // logToConsole('audio processed: ', data);
        logToConsole('processed text: ', data.text);
    }
    async function handleStoppedRecording(){
        console.log('number of chunks: ', recordedChunks.length);
        const blob = new Blob(recordedChunks, { type: 'audio/webm' });
        await uploadAudio(blob);
        audioStream = null;
        recordedChunks = [];
        audioRecorder = null;
        stream = null;
        logToConsole('handleStoppedRecording');
        document.querySelector('#startAudio').textContent = 'start';
    }
    async function startRecording(){
        if(audioStream){
            stopRecording();;
        }
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            audioEl.srcObject = stream;
            audioStream = stream;
            audioRecorder = new MediaRecorder(audioStream);
            audioRecorder.ondataavailable = function(event) {
                console.log('pushing chunk');
                recordedChunks.push(event.data);
            };
            audioRecorder.addEventListener('stop', async () => {
                console.log('audioRecorder stop event fired');
                handleStoppedRecording()
            })
            audioRecorder.start();
            const track = audioStream.getAudioTracks()[0];
    
            logToConsole('audio started');
            document.querySelector('#startAudio').textContent = 'stop';
        })
        .catch((error) => {
            console.error('Error accessing the audio:', error);
            logToConsole('Error accessing the audio', error);
        });
    }

    document.querySelector('#startAudio').addEventListener('click', startRecording);
})()