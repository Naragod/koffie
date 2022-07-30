from .routes import *


def main():
  try:
    app
  except Exception as e:
    print("AAAAAAAAAAAAAAAA")
    return {"message": "There was an unexpected error", "error": e}


main()
