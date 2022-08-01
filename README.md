to install required packages run the following: `pip install -r ./requirements.txt`

to set up sqlite3 db make sure that the file `setup.sh` has executable persmissions.
    If it does not execute the following command: `chmod +x setup.sh`
    Execute the setup.sh file to setup the local cache db.

to start up server run the following command: `clear; uvicorn src.index:app --reload`

to execute tests, run the following command: `python3 -m src.tests.main_tests`