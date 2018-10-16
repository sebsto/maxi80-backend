import unittest
import json
import os
from unittest.mock import Mock, patch
import warnings
import logging
import boto3
from maxi80_backend import app

LASTFM_API_KEY='a3286d25ccc61a3824bddd04d0d87593'
BUCKET='artwork.maxi80.com'
AWS_PROFILE='backend'

logging.basicConfig()
logger = logging.getLogger('TestMaxi80Backend')
logger.setLevel(logging.DEBUG)

@patch.dict(os.environ,{'LASTFM_API_KEY':LASTFM_API_KEY, 'BUCKET' : BUCKET, 'AWS_PROFILE' : AWS_PROFILE})
class TestMaxi80Backend(unittest.TestCase):

    def clean_cache(self, artist, track):
        s3 = boto3.client('s3')
        s3.delete_object(Bucket=BUCKET,Key="%s/%s/info.json" % (artist, track))
        s3.delete_object(Bucket=BUCKET,Key="%s/%s/cover.png" % (artist, track))

    def setUp(self):
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>") 
        warnings.filterwarnings("ignore", category=DeprecationWarning) 

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_happy_path_no_cache(self, mocker):

        # read APIGW event
        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        # ensure the S3 cache is empty 
        ARTIST = apigw_event['pathParameters']['artist']
        TRACK= apigw_event['pathParameters']['track']
        self.clean_cache(ARTIST, TRACK)

        # prepare request's reponse 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "cover.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    def test_lambda_handler_happy_path_with_cache(self):

        # read APIGW event
        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)
            artist_name = apigw_event['pathParameters']['artist']
            track_name= apigw_event['pathParameters']['track']
            s3 = boto3.resource('s3')
            s3.meta.client.upload_file('tests/lastfm.json', BUCKET, "%s/%s/info.json" % (artist_name, track_name))
            s3.meta.client.upload_file('tests/cover.png', BUCKET, "%s/%s/cover.png" % (artist_name, track_name))

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "cover.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_image_1(self, mocker):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        # ensure the S3 cache is empty 
        ARTIST = apigw_event['pathParameters']['artist']
        TRACK= apigw_event['pathParameters']['track']
        self.clean_cache(ARTIST, TRACK)

        # prepare requests' response
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.1.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "maxi80.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_image_2(self, mocker):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        # ensure the S3 cache is empty 
        ARTIST = apigw_event['pathParameters']['artist']
        TRACK= apigw_event['pathParameters']['track']
        self.clean_cache(ARTIST, TRACK)

        # prepare request' response 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.2.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "maxi80.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_image_3(self, mocker):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        # ensure the S3 cache is empty 
        ARTIST = apigw_event['pathParameters']['artist']
        TRACK= apigw_event['pathParameters']['track']
        self.clean_cache(ARTIST, TRACK)

        # prepare request' response 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.3.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "maxi80.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_image_4(self, mocker):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        # ensure the S3 cache is empty 
        ARTIST = apigw_event['pathParameters']['artist']
        TRACK= apigw_event['pathParameters']['track']
        self.clean_cache(ARTIST, TRACK)

        # prepare request' response 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.4.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "maxi80.png" in URL
        assert "AWSAccessKeyId" in URL
        assert "Signature" in URL

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_args_in_query_string(self, mocker):

        apigw_event = None
        with open('tests/event.no_path_parameters.json') as event_data:
            apigw_event = json.load(event_data)

        # prepare request' response 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.2.json') as lastfm_data:
            mocker.return_value.text = json.load(lastfm_data)

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 400

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_no_query_string(self, mocker):

        apigw_event = None
        with open('tests/event.no_path_parameters.json') as event_data:
            apigw_event = json.load(event_data)
            apigw_event["queryStringParameters"] = None

        # prepare request' response 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.noimage.2.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 400

    @patch('maxi80_backend.app.requests.get')
    def test_lambda_handler_track_not_found(self, mocker):

        # read APIGW event
        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)
            # the below two lines are not really necessary as we are mocking up LastFM's response.
            apigw_event['pathParameters']['artist'] ='XXX'
            apigw_event['pathParameters']['track'] = 'YYY'

        # prepare request's reponse 
        mocker.return_value.ok = True
        mocker.return_value.status_code = 200
        with open('tests/lastfm.not_found.json') as lastfm_data:
            mocker.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 404

    def test_lambda_handler_station(self):

            # read APIGW event
            apigw_event = None
            with open('tests/event.station.json') as event_data:
                apigw_event = json.load(event_data)

            ret = app.lambda_handler(apigw_event, "")
            assert ret["statusCode"] == 200
            body = json.loads(ret['body'])
            assert 'name' in body

if __name__ == '__main__':
    unittest.main()