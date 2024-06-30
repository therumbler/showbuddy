(function(){
let mediaStream;
let imageCapture;

function flipCamera() {
    if (!mediaStream) {
        logToConsole('Camera not started');
        return;
    }
    const video = document.getElementById('videoElement');
    const tracks = mediaStream.getVideoTracks();
    if (tracks.length === 0) {
        logToConsole('No video tracks found');
        return;
    }
    const track = tracks[0];
    const constraints = track.getConstraints();
    if (constraints.facingMode === 'user') {
        constraints.facingMode = 'environment';
    } else {
        constraints.facingMode = 'user';
    }
    track.applyConstraints(constraints)
    .then(() => {
        logToConsole(`Camera flipped to ${constraints.facingMode}`);
    })
    .catch((error) => {
        logToConsole('Error flipping camera');
        console.error('Error flipping camera:', error);
    });
}

function checkCamera() {
    if (!navigator.mediaDevices ) {
        logToConsole('mediaDevices not supported.');
        return;
    }

    if(!navigator.mediaDevices.enumerateDevices){
        logToConsole('enumerateDevices() not supported.');
        return;
    }

    // List cameras and microphones.
    navigator.mediaDevices.enumerateDevices()
    .then((devices) => {
        devices.forEach((device) => {
            logToConsole(`${device.kind}: ${device.label} id = ${device.deviceId}`);
        });
    })
    .catch((err) => {
        logToConsole('enumerateDevices() error: ' + err);
    });
}

function stopCamera() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => {
            track.stop();
        });
        logToConsole('Camera stopped');
    }
    mediaStream = null;
    document.querySelector('#start').textContent = 'start camera';
}
function startCamera() {
    // Get access to the camera!
    if(mediaStream){
        return stopCamera();
    }
    checkCamera()
    console.log('startCamera')
    const video = document.getElementById('videoElement');

    navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
        mediaStream = stream;
        const track = mediaStream.getVideoTracks()[0];

        imageCapture = new ImageCapture(track);
        logToConsole('Camera started');
        document.querySelector('#start').textContent = 'stop';
    })
    .catch((error) => {
        console.error('Error accessing the camera:', error);
        logToConsole('Error accessing the camera');
    });
}

function showCapturedPhoto(blob) {
  const url = URL.createObjectURL(blob);
  
  // Create a new Image element dynamically
  const img = new Image();
  img.onload = function() {
    URL.revokeObjectURL(url); // Release the object URL
  };
  img.src = url;
  
  // Display the image in a new window or modal (optional)
  // Example: open a new window with the image
  window.open(url, '_blank');
}

async function processCapturedPhoto(blob) {
    const formData = new FormData();
    formData.append('image', blob, 'photo.jpg');
    let resp = await fetch('/api/image', {
        method: 'POST',
        body: formData
    });
    if(!resp.ok){
        logToConsole('Error processing image');
        return;
    }
    let data = await resp.json();
    logToConsole('Image processed: ', data);
}

async function captureImage(){
    if (imageCapture) {
        let blob = await imageCapture.takePhoto();
        await processCapturedPhoto(blob);
    }
}
function captureImage2(){
    if (!mediaStream) {
        logToConsole('Camera not started');
        return;
    }
    const video = document.getElementById('videoElement');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');
    const img = document.createElement('img');
    img.src = dataUrl;
    document.body.appendChild(img);
    logToConsole('Image captured');
}

document.querySelector('#start').addEventListener('click', startCamera);
document.querySelector('#flip').addEventListener('click', flipCamera);
document.querySelector('#capture').addEventListener('click', captureImage);
})();