import AssemblyAI from "./assemblyai";
import { type File } from 'wasp/entities';

type ShowBuddyResponse = {
    status: string;
    text: string;
}

class ShowBuddy {
  private assemblyAI: AssemblyAI;

  constructor(apiKey: string|undefined) {
    if (!apiKey) {
      throw new Error('AssemblyAI API key is required');
    }
    this.assemblyAI = new AssemblyAI(apiKey);
  }
  
  async processAudio(file: File): Promise<ShowBuddyResponse> {
    // const audioUrl = await this.assemblyAI.uploadAudio(file);
    // const resp = await this.assemblyAI.getTranscription(audioUrl);
    return {'text': 'Hello World', 'status': 'success'};
  }
}

export default ShowBuddy;
export type { ShowBuddyResponse };