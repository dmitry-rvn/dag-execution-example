INSERT INTO rates (dt, currency_code, value)

SELECT
    '{dt}' AS dt,
    'EUR_TO_USD' AS currency_code,
    ROUND(eur.value / usd.value, 6) AS value
FROM (SELECT value FROM rates WHERE dt = '{dt}' AND currency_code = 'EUR') eur
JOIN (SELECT value FROM rates WHERE dt = '{dt}' AND currency_code = 'USD') usd
