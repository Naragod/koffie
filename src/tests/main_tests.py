import unittest
from unittest.mock import MagicMock, create_autospec, patch
from ..decoder import decode_vins


class MockResponse:
  def __init__(self, json_data):
    self.json_data = json_data
    print("json_data:", json_data)

  def json(self):
    return self.json_data


def mocked_post_request(data):
  return MockResponse(data)


class TestDecoder(unittest.TestCase):
  @patch('src.decoder.requests.get', side_effect=mocked_post_request)
  def test_decode_vins(self, _vins):
    test_vin = 'QWASZXQWASZX12345'
    expected_result = {
        'QWASZXQWASZX12345': {
            'vin': 'QWASZXQWASZX12345',
            'make': '',
            'model': '',
            'year': '',
            'body_class': ''
        }
    }
    result = decode_vins([test_vin])
    print("Result:", result)
    self.assertEqual(result, expected_result)


if __name__ == '__main__':
  print("AAAAAAAAAA")
  unittest.main()
