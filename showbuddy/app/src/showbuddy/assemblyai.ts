import axios from 'axios';

class AssemblyAI {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.assemblyai.com/v2';
  }

  public async uploadAudio(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${this.baseUrl}/upload`, formData, {
      headers: {
        'authorization': this.apiKey,
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data.upload_url;
  }

  async transcribeAudio(audioUrl: string): Promise<string> {
    const response = await axios.post(`${this.baseUrl}/transcript`, {
      audio_url: audioUrl
    }, {
      headers: {
        'authorization': this.apiKey,
        'Content-Type': 'application/json'
      }
    });

    return response.data.id;
  }

  async getTranscription(transcriptionId: string): Promise<any> {
    const response = await axios.get(`${this.baseUrl}/transcript/${transcriptionId}`, {
      headers: {
        'authorization': this.apiKey
      }
    });

    return response.data;
  }
}

export default AssemblyAI;