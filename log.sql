-- Keep a log of any SQL queries you execute as you solve the mystery.

-- This query get the necessary data for the crime, in description the interviews and bakery are mentioned
SELECT * FROM crime_scene_reports WHERE street='Humphrey Street' AND year=2021 AND month=7 AND day=28 AND description LIKE '%CS50%';

-- This query gets the data for the interviews
SELECT * FROM interviews WHERE year=2021 AND month=7 AND day=28 AND transcript LIKE '%thief%';

-- This query gets the license_plates of the cars that left the bakery at the time designated by one of the respondents
SELECT license_plate FROM bakery_security_logs WHERE year=2021 AND month=7 AND day=28 AND hour = 10 AND minute >= 15 AND minute <= 2
5 AND activity = 'exit';

-- This query get the calls that were done on the day of the crime, according to the qriteria given by one of the respondents
SELECT caller FROM phone_calls WHERE year=2021 AND month=7 AND day=28 AND duration <= 60;

-- This query gets the passport_number passengers for the earliest flight for the next day out of Fiftyville, ordered by time
SELECT passport_number FROM passengers WHERE flight_id in (SELECT flights.id FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year=2021 AND month=7 AND day=29 ORDER BY hour LIMIT 1);

-- This query get he person_id-s of the people that have withdrawn the money at the designated place
SELECT person_id FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number WHERE year=2021 AND month=7 AND day=28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- This query uses the previous queries to find the thief - it seems that it is Bruce
SELECT * FROM people
WHERE id in (SELECT person_id FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number WHERE year=2021 AND month=7 AND day=28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')
AND passport_number in (SELECT passport_number FROM passengers WHERE flight_id in (SELECT flights.id FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year=2021 AND month=7 AND day=29 ORDER BY hour LIMIT 1))
AND phone_number in (SELECT caller FROM phone_calls WHERE year=2021 AND month=7 AND day=28 AND duration <= 60)
AND license_plate in (SELECT license_plate FROM bakery_security_logs WHERE year=2021 AND month=7 AND day=28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit');

-- This query will check with whom Bruce has spoken to after the crime - it seems that it is Robin
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year=2021 AND month=7 AND day=28 AND duration <= 60 AND caller = '(367) 555-5533');

-- This query gets the destination city for Bruce
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE id = (SELECT flight_id FROM passengers WHERE passport_number = '5773159633'));
