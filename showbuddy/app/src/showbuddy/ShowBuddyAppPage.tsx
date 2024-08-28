import { useState, useRef } from 'react';
import { createFile, processAudioFile} from 'wasp/client/operations';
import axios from 'axios';

export default function ShowBuddyAppPage() {
  const [status, setStatus] = useState('stopped');
  const audioEl = document.querySelector('#audioElement') as HTMLAudioElement;
  const audioRef = useRef<HTMLAudioElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  let audioStream: MediaStream;
  let audioRecorder: MediaRecorder;
  let recordedChunks: Blob[] = [];
  const uploadAudio = async (file: Blob) => {
    const formData = new FormData();
    formData.append('file', file);
    if (!file || !file.type) {
      throw new Error('No file selected');
    }

    const fileType = file.type;
    const name = 'audio.webm';

    const { uploadUrl } = await createFile({ fileType, name });
    if (!uploadUrl) {
      throw new Error('Failed to get upload URL');
    }
    const res = await axios.put(uploadUrl, file, {
      headers: {
        'Content-Type': fileType,
      },
    });
    if (res.status !== 200) {
      throw new Error('File upload to S3 failed');
    }
    return res;
  }
  
  const processAudio = async (file: Blob) => {
    console.log('processing audio');
    const res = await uploadAudio(file);
    console.log('upload response', res);
    const audioUrl = res.config.url;
    const resp = await processAudioFile({audioUrl});
    
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
    if(!audioRef.current){
      console.error('audioRef is null');
      return
    }
    console.log('startRecording');
    audioRef.current.srcObject = stream;
    audioStream = stream;
    audioRecorder = new MediaRecorder(audioStream);
    mediaRecorderRef.current = audioRecorder;
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
      if(!mediaRecorderRef.current){
        console.error('mediaRecorderRef is null');
        return
      }
      setStatus('stopped');
      console.log('stopping recording audioRecorder:', audioRecorder);  
      mediaRecorderRef.current.stop();
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
              <audio id="audioElement" ref={audioRef}></audio>
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
