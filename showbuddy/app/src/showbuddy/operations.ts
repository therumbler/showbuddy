import { HttpError } from 'wasp/server';
import ShowBuddy from './showbuddy';
import { ShowBuddyResponse } from './showbuddy';
import { type File } from 'wasp/entities';

import { 
    type ProcessAudioFile, 
    type CreateFile,
    type getDownloadFileSignedURL 
} from 'wasp/server/operations';

import {
    getUploadFileSignedURLFromS3,
    getDownloadFileSignedURLFromS3
  } from './s3Utils';

type showBuddyInput = {
    audioUrl: string;
};

type FileDescription = {
    fileType: string;
    name: string;
  };

export const processAudioFile: ProcessAudioFile<showBuddyInput, ShowBuddyResponse> = async ({ audioUrl }, context) => {
    if (!context.user) {
        throw new HttpError(401);
    }
    
    console.log('audioUrl', audioUrl);
    const userInfo = context.user.id;
    const showBuddy = new ShowBuddy(process.env.ASSEMBLY_AI_API_KEY);
    console.log('showBuddy instance', showBuddy);
    const resp =  await showBuddy.processAudio(audioUrl);
    return resp;
};


export const createFile: CreateFile<FileDescription, File> = async ({ fileType, name }, context) => {
    if (!context.user) {
      throw new HttpError(401);
    }
  
    const userInfo = context.user.id;
  
    const { uploadUrl, key } = await getUploadFileSignedURLFromS3({ fileType, userInfo });
  
    return await context.entities.File.create({
      data: {
        name,
        key,
        uploadUrl,
        type: fileType,
        user: { connect: { id: context.user.id } },
      },
    });
  };