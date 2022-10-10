INSERT INTO rates (dt, currency_code, value)

SELECT
    '{dt}' AS dt,
    'USD_TO_EUR' AS currency_code,
    ROUND(1 / value, 6) AS value
FROM rates
WHERE dt = '{dt}' AND currency_code = 'EUR_TO_USD'
