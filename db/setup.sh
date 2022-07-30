

echo "Initalizing db setup."
curr_path=$(pwd)

# remove db if it already exists
rm $curr_path/db/koffie_db 2> /dev/null

# create koffie_db database
echo "Creating database."
sqlite3 $curr_path/db/koffie_db < $curr_path/db/setup.sql

echo "Database created."
