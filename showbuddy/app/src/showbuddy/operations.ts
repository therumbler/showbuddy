import { HttpError } from 'wasp/server';
import ShowBuddy from './showbuddy';
import { ShowBuddyResponse } from './showbuddy';
import { type File } from 'wasp/entities';

import { type ProcessAudioFile } from 'wasp/server/operations';


type showBuddyInput = {
    file: File,
    context: any,
};

type FileDescription = {
    fileType: string;
    name: string;
  };

export const processAudioFile: ProcessAudioFile<FileDescription, File> = async ({ fileType, name }, context) => {
// export const processAudioFile: ProcessAudioFile<ShowBuddyResponse> = async ({file} , context) => {
    if (!context.user) {
        throw new HttpError(401);
    }
    console.log('fileType', fileType);
    const userInfo = context.user.id;
    // const showBuddy = new ShowBuddy(process.env.ASSEMBLY_AI_API_KEY);
    // const resp =  await showBuddy.processAudio(file);
    return null;
    // const { uploadUrl, key } = await getUploadFileSignedURLFromS3({ fileType, userInfo });
    
    // return await context.entities.File.create({
    //     data: {
    //     name,
    //     key,
    //     uploadUrl,
    //     type: fileType,
    //     user: { connect: { id: context.user.id } },
    //     },
    // });
};
