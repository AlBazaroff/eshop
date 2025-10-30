echo "Start collecting static files"
python3 eshop/manage.py collectstatic
echo "End collecting static files"

echo "Start migrations"
python3 eshop/manage.py makemigrations
python3 eshop/manage.py migrate
echo "End migrations

# Future
# add filling by testing data
# add settings files