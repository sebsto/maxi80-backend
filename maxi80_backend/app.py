import json
import os
import logging
import requests
import boto3
from botocore.exceptions import ClientError

logging.basicConfig()
logger = logging.getLogger('Maxi80Backend')

# logging level
logger.setLevel(logging.INFO)
log_level = os.environ.get('LOG_LEVEL')
if log_level != None:
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        print('Invalid log level: %s' % log_level)
    else:
        logger.setLevel(numeric_level)

def get_artwork_url(artist, track, lastfm ):

    def defaultImage():
        # no track or album
        # no extralarge or lastfm returned /noimage/ 
        # return the maxi80 placeholder
        logger.debug('no image found')
        s3 = boto3.client('s3')
        return s3.generate_presigned_url('get_object', Params = {'Bucket': os.environ["BUCKET"], 'Key': 'maxi80.png'}, ExpiresIn = 60)

    # find the extrallarge image 
    result = None
    try:
        large_url = list(filter(lambda x: x["size"] == 'extralarge', lastfm["track"]["album"]["image"]))

        if len(large_url) == 0 or len(large_url) > 1 or "/noimage/" in large_url[0]["#text"] or len(large_url[0]["#text"]) == 0:
            result = defaultImage()
        else:

            # found an extra large image
            logger.debug('image found')

            s3 = boto3.client('s3')
            BUCKET = os.environ["BUCKET"]
            key = "%s/%s/cover.png" % (artist, track)
            try:
                # there is a large cover returned, do we have it already on S3 ?
                s3.get_object(Bucket=BUCKET, Key=key)

                # yes, compute the signed URL and return
                logger.debug('image in cache, returning presigned URL')
                result = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': key}, ExpiresIn = 60)
                
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':

                    # no, download it from last fm 
                    logger.debug('image not in cache, downloading it from URL returned by LastFM')
                    import urllib.request 
                    urllib.request.urlretrieve(large_url[0]['#text'], '/tmp/cover.png')     

                    # upload it to S3
                    s3.upload_file('/tmp/cover.png', BUCKET, key, ExtraArgs={"ContentType": "image/png"})

                    # and generate the pre-signed url    
                    logger.debug('image is now in cache, returning presigned URL')
                    result = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': key}, ExpiresIn = 60)
                else:
                    raise ex
    except:
        result = defaultImage()

    return result

def lambda_handler(event, context):
    '''
        Maxi80 Backend

        /artwork 
            fetch the artwork from LastFM
            use S3 as cache
    '''

    # http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=a3286d25ccc61a3824bddd04d0d87593&artist=Phil%20Collins&track=Easy%20Lover&format=json

    result = None 
    logger.debug(json.dumps(event))
    if "path" not in event: 
        result = { 'body' : json.dumps({
                'error' :  'invalid parameters', 
                'possible_cause' : 'path must start with either /artwork or /station'
                }),   
                'statusCode' : 400} 
    
    if event['path'].startswith("/artwork"):
        result = artwork(event,context)

    if event['path'].startswith("/station"):
        result = station(event, context)

    logger.debug(json.dumps(result))
    return result


def station(event, context):

    STATION=  { 'name': "Maxi80",
            'streamURL': "https://audio1.maxi80.com",
            'imageURL': "station-maxi80.png",
            'desc': "La radio de toute une génération",
            'longDesc': "Le meilleur de la musique des années 80"}

    return  { 'statusCode' : 200, 'body' : json.dumps(STATION) }          

def artwork(event, context):   

    # sanity check on path params and query string 
    if ("pathParameters" not in event) or (event["pathParameters"] == None) or ("artist" not in event["pathParameters"]) or ("track" not in event["pathParameters"]):
        logger.debug("no path parameters artist or track")
        
        return { 'body' : json.dumps({
                'error' :  'invalid parameters', 
                'possible_cause' : 'Did you specify "artist" and "track" in the path ?  For example : GET /artwork/artist/track'
                }),   
                'statusCode' : 400}

        # if ("queryStringParameters" not in event) or (event["queryStringParameters"] == None) or ("artist" not in event["queryStringParameters"]) or ("track" not in event["queryStringParameters"]):
        #     logger.debug("no query string parameters artist or track")
        #     return { 'body' : json.dumps({
        #             'error' :  'invalid parameters', 
        #             'possible_cause' : 'Did you specify "artist" and "track" in the path or query string?'
        #             }),   
        #             'statusCode' : 400}
        # else:
        #     ARTIST=event["queryStringParameters"]["artist"]
        #     TRACK=event["queryStringParameters"]["track"]
    else:
        ARTIST=event["pathParameters"]["artist"]
        TRACK=event["pathParameters"]["track"]

    lastFM_response = None 

    try:
        LASTFM_API_KEY = os.environ["LASTFM_API_KEY"]
        BUCKET = os.environ["BUCKET"]

        result = { 'statusCode' : 0, 'body' : ''}
        key = "%s/%s/info.json" % (ARTIST, TRACK)
        s3 = boto3.client('s3')
        
        try:
            # do we have data on S3 ?
            logger.debug("Checking cache on %s/%s" % (BUCKET, key))
            info = s3.get_object(Bucket=BUCKET, Key=key)

            logger.debug('Object found on S3')
            result["statusCode"] = 200
            lastFM_response = json.loads(info["Body"].read().decode('UTF-8'))

        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':

                # we don't have data on S3, let's query LastFM API
                logger.debug('No object found : %s - querying LastFM' % key)
                response = requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=%s&artist=%s&track=%s&format=json" % (LASTFM_API_KEY, ARTIST, TRACK))
                result["statusCode"] = response.status_code
                logger.debug('LastFM responded with code : %d' % response.status_code)
                lastFM_response = json.loads(response.text)
                logger.debug(response.text)

                if "error" in lastFM_response:
                    # do not cache, probably incorrect track name. 
                    result["statusCode"] = 404 # should we return 500 ?
                    result["error"] = response.text

                    # return a default image 
                    result["body"] = { 'url' : get_artwork_url(ARTIST, TRACK, lastFM_response),
                                       'artist' : ARTIST,
                                       'track' : TRACK }
                else:
                    # and save it to S3
                    s3.put_object(Bucket=BUCKET, Key=key, Body=response.text.encode('UTF-8'))

            else:
                logger.error(ex)
                raise ex  

    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        logger.error(e)
        raise e
    except KeyError as e:
        # Send some context about this error to Lambda Logs
        logger.error(e)
        raise e

    # replace body with URL of the artwork (either downloaded or taken from cache)
    if result['statusCode'] == 200:
        result['body'] = json.dumps({ 'url' : get_artwork_url(ARTIST, TRACK, lastFM_response),
        'artist' : ARTIST,
        'track' : TRACK })

    return result

