INSERT INTO rates (dt, currency_code, value)

SELECT
    '{dt}' AS dt,
    'CURR_BASKET' AS currency_code,
    ROUND(EXP(SUM(LN(POWER(value, ratio)))), 4) AS value
FROM rates r
JOIN currency_basket b ON b.currency_code = r.currency_code
WHERE dt = '{dt}'
