import json
import boto3
import os
import uuid

def speak(event, context):   

    """
    Synthesizes speech from the input string of text and
    returns the output as an Amazon S3 object
    """

    try:
        data = json.loads(event['body'])
        text_to_synthesize = data['text']
        voice_id = data.get('voice', 'Joanna')  # Default to Joanna if 'voice' is not provided
    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow CORS for all domains
            },
            'body': json.dumps({'error': f'Missing required parameter: {str(e)}'})
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow CORS for all domains
            },
            'body': json.dumps({'error': f'Invalid JSON payload: {str(e)}'})
        }
    
    polly_client = boto3.client('polly')
    
    response = polly_client.synthesize_speech(
        Text=text_to_synthesize,
        OutputFormat='mp3',
        VoiceId=voice_id
    )

    # Step 2: Save the audio stream to an S3 bucket
    s3_bucket_name = 'talking-app-bucket'
    file_key = f'audio/{str(uuid.uuid1())}.mp3'   #Check to see which uuid is being used
    
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=response['AudioStream'].read(),
        Bucket=s3_bucket_name,
        Key=file_key
    )

    # Step 3: Get a signed URL for the saved MP3 file
    signed_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3_bucket_name, 'Key': file_key},
        ExpiresIn=3600  # URL expiration time in seconds
    )
    
    # Return the signed URL to the front end application
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow CORS for all domains
            },
        'body': json.dumps({
            'signed_url': signed_url
        })
    }
