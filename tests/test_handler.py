import unittest
import json
import os
from unittest.mock import Mock, patch, call
import warnings
import logging
from botocore.exceptions import ClientError
from src import app
from src.app import build_key

LASTFM_API_KEY='a3286d25ccc61a3824bddd04d0d87593'
BUCKET='artwork.maxi80.com'
AWS_PROFILE='maxi80'
NO_COVER_IMAGE="no-cover-400x400.png"

logging.basicConfig()
logger = logging.getLogger('TestMaxi80Backend')
logger.setLevel(logging.DEBUG)

@patch.dict(os.environ,{'LASTFM_API_KEY':LASTFM_API_KEY, 'BUCKET' : BUCKET, 'AWS_PROFILE' : AWS_PROFILE})
class TestMaxi80Backend(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    @patch('src.app.urllib.request.urlretrieve')
    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_happy_path_no_cache(self, mock_requests_get, mock_boto3_client, mock_urlretrieve):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        ARTIST = apigw_event['pathParameters']['artist']
        TRACK = apigw_event['pathParameters']['track']

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        # cache miss on both info.json and cover.png
        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{ARTIST}/{TRACK}/cover.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "cover.png" in URL

    @patch('src.app.urllib.request.urlretrieve')
    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_with_encoding_no_cache(self, mock_requests_get, mock_boto3_client, mock_urlretrieve):

        apigw_event = None
        with open('tests/event.with.encoding.json') as event_data:
            apigw_event = json.load(event_data)

        ARTIST = apigw_event['pathParameters']['artist']
        TRACK = apigw_event['pathParameters']['track']

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{ARTIST}/{TRACK}/cover.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.with.encoding.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "cover.png" in URL

    @patch('src.app.boto3.client')
    def test_lambda_handler_happy_path_with_cache(self, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        ARTIST = apigw_event['pathParameters']['artist']
        TRACK = apigw_event['pathParameters']['track']

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        # cache hit: return valid info.json and cover.png
        with open('tests/lastfm.json') as f:
            info_body = Mock()
            info_body.read.return_value = f.read().encode('UTF-8')

        mock_s3.get_object.return_value = {"Body": info_body}
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{ARTIST}/{TRACK}/cover.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert "cover.png" in URL

    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_no_image_1(self, mock_requests_get, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{NO_COVER_IMAGE}"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.noimage.1.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert NO_COVER_IMAGE in URL

    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_no_image_2(self, mock_requests_get, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{NO_COVER_IMAGE}"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.noimage.2.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert NO_COVER_IMAGE in URL

    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_no_image_3(self, mock_requests_get, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{NO_COVER_IMAGE}"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.noimage.3.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert NO_COVER_IMAGE in URL

    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_no_image_4(self, mock_requests_get, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{NO_COVER_IMAGE}"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.noimage.4.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert NO_COVER_IMAGE in URL

    def test_lambda_handler_no_args_in_query_string(self):

        apigw_event = None
        with open('tests/event.no_path_parameters.json') as event_data:
            apigw_event = json.load(event_data)

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 400

    def test_lambda_handler_no_query_string(self):

        apigw_event = None
        with open('tests/event.no_path_parameters.json') as event_data:
            apigw_event = json.load(event_data)
            apigw_event["queryStringParameters"] = None

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 400

    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    def test_lambda_handler_track_not_found(self, mock_requests_get, mock_boto3_client):

        apigw_event = None
        with open('tests/event.json') as event_data:
            apigw_event = json.load(event_data)
            apigw_event['pathParameters']['artist'] = 'XXX'
            apigw_event['pathParameters']['track'] = 'YYY'

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{NO_COVER_IMAGE}"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.not_found.json') as lastfm_data:
            mock_requests_get.return_value.text = lastfm_data.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        assert ret["lastFMStatusCode"] == 404
        body = json.loads(ret['body'])
        assert 'url' in body
        URL = body['url']
        assert "https://" in URL
        assert NO_COVER_IMAGE in URL

    @patch('src.app.urllib.request.urlretrieve')
    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    @patch.dict(os.environ, {'KEY_PREFIX': ''})
    def test_lambda_handler_empty_prefix_backward_compatible(self, mock_requests_get, mock_boto3_client, mock_urlretrieve):
        """With KEY_PREFIX='', S3 keys must be identical to the original format (no prefix)."""

        with open('tests/event.json') as f:
            apigw_event = json.load(f)

        ARTIST = apigw_event['pathParameters']['artist']
        TRACK = apigw_event['pathParameters']['track']

        expected_info_key = f"{ARTIST}/{TRACK}/info.json"
        expected_cover_key = f"{ARTIST}/{TRACK}/cover.png"

        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/{ARTIST}/{TRACK}/cover.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.json') as f:
            mock_requests_get.return_value.text = f.read()

        ret = app.lambda_handler(apigw_event, "")

        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'url' in body
        assert "cover.png" in body['url']

        get_object_keys = [c[1]['Key'] for c in mock_s3.get_object.call_args_list]
        assert expected_info_key in get_object_keys
        assert expected_cover_key in get_object_keys

        mock_s3.put_object.assert_called_once()
        assert mock_s3.put_object.call_args[1]['Key'] == expected_info_key

        mock_s3.upload_file.assert_called_once()
        assert mock_s3.upload_file.call_args[0][2] == expected_cover_key

        presigned_keys = [c[1]['Params']['Key'] for c in mock_s3.generate_presigned_url.call_args_list]
        assert expected_cover_key in presigned_keys

    @patch('src.app.urllib.request.urlretrieve')
    @patch('src.app.boto3.client')
    @patch('src.app.requests.get')
    @patch.dict(os.environ, {'KEY_PREFIX': 'v1/'})
    def test_lambda_handler_v1_prefix_all_key_types(self, mock_requests_get, mock_boto3_client, mock_urlretrieve):
        """With KEY_PREFIX='v1/', all three S3 key types must start with 'v1/'."""

        with open('tests/event.json') as f:
            apigw_event = json.load(f)

        ARTIST = apigw_event['pathParameters']['artist']
        TRACK = apigw_event['pathParameters']['track']

        expected_info_key = f"v1/{ARTIST}/{TRACK}/info.json"
        expected_cover_key = f"v1/{ARTIST}/{TRACK}/cover.png"
        expected_no_cover_key = "v1/no-cover-400x400.png"

        # --- Part 1: Happy path (cover image found, cache miss) ---
        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/v1/{ARTIST}/{TRACK}/cover.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.json') as f:
            mock_requests_get.return_value.text = f.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200

        get_object_keys = [c[1]['Key'] for c in mock_s3.get_object.call_args_list]
        assert expected_info_key in get_object_keys
        assert expected_cover_key in get_object_keys
        assert mock_s3.put_object.call_args[1]['Key'] == expected_info_key
        assert mock_s3.upload_file.call_args[0][2] == expected_cover_key

        # --- Part 2: No-cover path ---
        mock_s3.reset_mock()
        mock_requests_get.reset_mock()
        mock_urlretrieve.reset_mock()

        mock_s3.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Not Found'}}, 'GetObject'
        )
        mock_s3.generate_presigned_url.return_value = (
            f"https://{BUCKET}.s3.amazonaws.com/v1/no-cover-400x400.png"
            "?AWSAccessKeyId=FAKE&Signature=FAKE&Expires=9999"
        )

        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.status_code = 200
        with open('tests/lastfm.noimage.1.json') as f:
            mock_requests_get.return_value.text = f.read()

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200

        presigned_keys = [c[1]['Params']['Key'] for c in mock_s3.generate_presigned_url.call_args_list]
        assert expected_no_cover_key in presigned_keys

    def test_build_key_defaults_to_empty_when_not_set(self):
        """When KEY_PREFIX is not set in the environment, build_key defaults to empty string."""
        os.environ.pop('KEY_PREFIX', None)

        assert build_key("some/suffix.txt") == "some/suffix.txt"
        assert build_key("no-cover-400x400.png") == "no-cover-400x400.png"
        assert build_key("artist/track/cover.png") == "artist/track/cover.png"

    def test_lambda_handler_station(self):

        apigw_event = None
        with open('tests/event.station.json') as event_data:
            apigw_event = json.load(event_data)

        ret = app.lambda_handler(apigw_event, "")
        assert ret["statusCode"] == 200
        body = json.loads(ret['body'])
        assert 'name' in body
        assert 'streamURL' in body
        assert 'donationURL' in body
        assert 'websiteURL' in body

if __name__ == '__main__':
    unittest.main()
