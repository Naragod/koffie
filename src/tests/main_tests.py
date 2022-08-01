import unittest
from fastapi.testclient import TestClient

from ..cache import Cache
from ..decoder import Decoder
from ..routes import app
from unittest.mock import patch
import json


client = TestClient(app)


class TestEndpoints(unittest.TestCase):

  @patch.object(Cache, "query")
  @patch.object(Cache, "close")
  @patch.object(Cache, "commit")
  @patch.object(Cache, "__init__")
  def test_incorrect_vin_lookup(self, init, commit, close, query):
    init.return_value = None
    commit.return_value = None
    close.return_value = None
    query.return_value = None

    response = client.get("/lookup/123")
    response_content = json.loads(response.content)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response_content["detail"], "Invalid Vin")

  @patch.object(Cache, "query")
  @patch.object(Cache, "close")
  @patch.object(Cache, "commit")
  @patch.object(Cache, "__init__")
  def test_correct_vin_lookup_vin_is_cached(self, init, commit, close, query):
    expected_response = [('QWASZXQWASZX12345', 'make', 'model', 'year', 'class')]
    init.return_value = None
    commit.return_value = None
    close.return_value = None
    query.return_value = expected_response

    response = client.get("/lookup/QWASZXQWASZX12345")
    response_content = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_content, [['QWASZXQWASZX12345', 'make', 'model', 'year', 'class', True]])

  @patch.object(Cache, "query")
  @patch.object(Cache, "close")
  @patch.object(Cache, "commit")
  @patch.object(Cache, "__init__")
  @patch.object(Decoder, "decode_vins")
  def test_correct_vin_lookup_vin_is_not_cached(self, decode_vins, init, commit, close, query):
    expected_response = {
        '1XPWD40X1ED215307': {
            'vin': '1XPWD40X1ED215307',
            'make': 'PETERBILT',
            'model': '388',
            'year': '2014',
            'body_class':
            'Truck-Tractor'
        }
    }
    init.return_value = None
    commit.return_value = None
    close.return_value = None
    query.return_value = []
    decode_vins.return_value = expected_response

    response = client.get("/lookup/QWASZXQWASZX12345")
    response_content = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response_content, expected_response)


if __name__ == '__main__':
  print("Running unit tests...")
  unittest.main()
  print("All unit tests have finished.")
