# Show Buddy


## Show Buddy - Transcribe Trade Show Conversations

## Requirements
1. Docker 
2. An S3 compatible API running, with a bucket called "showbuddy"


## How to run
1. Create a `.env` file with the following environment variables

```
AWS_ENDPOINT_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
SPREADLY_API_KEY=
ASSEMBLYAI_API_KEY=
```

2. run `make run-docker`


## Testing

to test that your local instance is working run the below `curl` comand:
```
curl \
    -F "audio=@./tests/integration/files/test_audio_1a.m4a" \
    -F "image=@./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg" \
http://127.0.0.1:5019/api/process
```