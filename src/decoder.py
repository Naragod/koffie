import requests
import json
from urllib.parse import urljoin


class Decoder:
  def __init__(self, base_url):
    self.base_url = base_url

  def decode_vins(self, vins):
    result = {}
    formatted_vins = ";".join(vins)
    url = urljoin(self.base_url, "vehicles/DecodeVINValuesBatch")
    post_fields = {'format': 'json', 'data': formatted_vins}
    response = requests.post(url, data=post_fields)
    json_response = json.loads(response.text)
    vin_results = json_response["Results"]

    for item in vin_results:
      result[item["VIN"]] = {
          "vin": item["VIN"],
          "make": item["Make"],
          "model": item["Model"],
          "year": item["ModelYear"],
          "body_class": item["BodyClass"],
      }

    return result
