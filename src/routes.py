from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pyarrow as pa
import pandas as pd
import pyarrow.parquet as pq
from .decoder import *
from .cache import Cache
import pathlib

app = FastAPI()
base__vin_decoder_url = 'https://vpic.nhtsa.dot.gov/api/'
home_dir = str(pathlib.Path(__file__).resolve().parents[1])
decoder = Decoder(base__vin_decoder_url)


@ app.get("/lookup/{vin}")
def lookup_vin(vin: str):
  try:
    # check cache. If vin exits return
    cache = Cache(home_dir + "/db" + "/koffie_db", True)

    if(len(vin) != 17):
      raise HTTPException(status_code=404, detail="Invalid Vin")
    cached_result = cache.query("select * from vehicle where vin = ?", (vin,))

    if(cached_result is not None and len(cached_result) > 0):
      cached_result[0] += (True,)
      return cached_result
    # call vPIC endpoint
    decoded_vins = decoder.decode_vins([vin])

    for item in decoded_vins:
      insert_values = ()

      for val in list(decoded_vins[item].items()):
        insert_values += (val[1], )
      cache.query("INSERT INTO vehicle VALUES (?, ?, ?, ?, ?)", insert_values)
    return decoded_vins
  except Exception as e:
    raise e
  finally:
    cache.commit()
    cache.close()


@app.get("/export", response_class=FileResponse)
def export_vehicle_cache():
  try:
    json_df = {"vin": [], "make": [], "model": [], "year": [], "body_class": [], }
    cache = Cache(str(home_dir) + "/db" + "/koffie_db", True)
    result = cache.query("select * from vehicle")

    for item in result:
      json_df["vin"].append(item[0])
      json_df["make"].append(item[1])
      json_df["model"].append(item[2])
      json_df["year"].append(item[3])
      json_df["body_class"].append(item[4])
    df = pd.DataFrame(data=json_df)
    table = pa.Table.from_pandas(df)
    table_file_location = home_dir + "/exports" + "/result.parquet"
    pq.write_table(table, table_file_location)
    return table_file_location

  except Exception as e:
    print("Could not export cached data to file.")
    raise e


@app.delete("/remove/{vin}")
def remove_vin_from_cache(vin: str):
  try:
    success = False
    # check cache. If vin exits remove it and return
    cache = Cache(str(home_dir) + "/db" + "/koffie_db", True)

    if(len(vin) != 17):
      raise HTTPException(status_code=404, detail="Invalid Vin")
    cache.query("DELETE FROM vehicle where vin = ?", (vin,))
    cached_result = cache.query("select count(*) from vehicle where vin = ?", (vin,))

    if(cached_result[0][0] == 0):
      success = True
    return {"cache_delete_success": success, "vin": vin}

  except Exception as e:
    print("Could not remove vin from cache:", vin)
    raise e
  finally:
    cache.commit()
    cache.close()
