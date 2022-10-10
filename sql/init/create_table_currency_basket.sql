DROP TABLE IF EXISTS currency_basket;

CREATE TABLE currency_basket (
   	currency_code TEXT NOT NULL,
	ratio REAL NOT NULL
);

INSERT INTO currency_basket VALUES
    ('RUB', 0.5),
    ('USD', 0.3),
    ('EUR', 0.1),
    ('CNY', 0.1);
