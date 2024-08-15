import boto3
import json
import base64

def lambda_handler(event, context):
    polly = boto3.client('polly')

    # Extract text from the event
    text = event['queryStringParameters']['text']

    # Convert text to speech
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Brian'
    )

    # Read the audio stream
    audio_stream = response['AudioStream'].read()

    # Return the audio stream as Base64 encoded string
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',  # Use application/json for JSON response
        },
        'body': json.dumps({
            'audio': base64.b64encode(audio_stream).decode('utf-8')  # Encode audio as Base64 and include in JSON
        }),
        'isBase64Encoded': False  # False, since body is a JSON string, not Base64 encoded data
    }
