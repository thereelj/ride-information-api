# ride-information-api
A RESTful API using Django REST Framework for managing ride information


Steps to run:
Python version requirements: Python 3.9.6

1.) Ensure docker and docker compose is installed

2.) Make sure docker.desktop is up and running

3.) Run docker compose build

4.) Run docker compose up -d

5.) If the setup is successful, open http://localhost/admin on your browser

6.) To create superuser: docker compose run --rm app sh -c "python manage.py createsuperuser"


Additional notes:
- Added 'distance' field on response when having GPS position as input to capture the difference between the two points.


Bonus - SQL:

WITH pickup AS (
    SELECT id_ride_id AS id_ride, created_at AS pickup
    FROM core_rideevent
    WHERE description = 'Status changed to pickup'
),
dropoff AS (
    SELECT id_ride_id AS id_ride, created_at AS dropoff
    FROM core_rideevent
    WHERE description = 'Status changed to dropoff'
),
more_than_one_hour AS (
    SELECT p.id_ride
    FROM pickup p
    INNER JOIN dropoff d ON p.id_ride = d.id_ride
    WHERE EXTRACT(EPOCH FROM (d.dropoff - p.pickup)) / 60 > 60
),
with_driver AS (
    SELECT 
        TO_CHAR(r.pickup_time, 'YYYY-MM') AS month,
        CONCAT(u.first_name, ' ', SUBSTRING(u.last_name, 1, 1)) AS driver,
        r.id AS id_ride
    FROM more_than_one_hour m
    LEFT JOIN core_ride r ON m.id_ride = r.id
    LEFT JOIN core_user u ON u.id = r.id_driver_id
)
SELECT 
    month AS "Month", 
    driver AS "Driver", 
    COUNT(id_ride) AS "Count of Trips > 1 hr"
FROM with_driver
GROUP BY month, driver
ORDER BY month, driver;

