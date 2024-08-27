import {useState} from 'react';

export default function ShowBuddyAppPage() {
  const [status, setStatus] = useState('stopped');
  const audioEl = document.querySelector('#audioElement') as HTMLAudioElement;
  let audioStream: MediaStream;
  let audioRecorder: MediaRecorder;
  let recordedChunks: Blob[] = [];
  const processAudio = async (blob: Blob) => {
    console.log('processing audio');
  }
  const handleStoppedRecording = async (evt: Event) => {
    console.log('number of chunks: ', recordedChunks.length);
    const blob = new Blob(recordedChunks, { type: 'audio/webm' });
    await processAudio(blob);
    audioStream.getTracks;
    recordedChunks = [];
    // audioRecorder = null;
    audioRecorder.stop();
    // audioRecorder.getTracks().forEach(track => track.stop());
    // logToConsole('handleStoppedRecording');
    // document.querySelector('#startAudio').textContent = 'start';
    setStatus('stopped');
  } 
  const startRecording = (stream: MediaStream) => {
    audioEl.srcObject = stream;
    audioStream = stream;
    audioRecorder = new MediaRecorder(audioStream);
    audioRecorder.ondataavailable = function(event) {
        console.log('pushing chunk');
        recordedChunks.push(event.data);
    };
    audioRecorder.addEventListener('stop', async (evt) => {
        console.log('audioRecorder stop event fired');
        handleStoppedRecording(evt)
    })
    audioRecorder.start();
   

    setStatus('recording');     
    }

  const handleRecordingButton = async () => {
    if (status === 'recording') {
      setStatus('stopped');
      return;
    }
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            startRecording(stream);
        })
    setStatus('recording');
  }
  return (
    <div className='flex min-h-full flex-col justify-center mt-10 sm:px-6 lg:px-8'>
      <div className='sm:mx-auto sm:w-full sm:max-w-md'>
        <div className='py-8 px-4 shadow-xl ring-1 ring-gray-900/10 dark:ring-gray-100/10 sm:rounded-lg sm:px-10'>
          <h1>Show Buddy App</h1>
          
          <form>
            <div id="showbuddyapp" className='mt-6'>
              <audio id="audioElement"></audio>
              <button id="startAudio" type="button" onClick={handleRecordingButton} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                {status === 'recording' ? 'Stop Recording' : 'Start Recording'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
