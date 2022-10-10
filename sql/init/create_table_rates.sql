DROP TABLE IF EXISTS rates;

CREATE TABLE rates (
	dt TEXT NOT NULL,
   	currency_code TEXT NOT NULL,
	value REAL NOT NULL,
	sysmoment TEXT DEFAULT (DATETIME('now')),
	UNIQUE(dt, currency_code)
);
