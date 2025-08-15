BEGIN;

CREATE TABLE IF NOT EXISTS users (
	id            SERIAL PRIMARY KEY,
	telegram_id   BIGINT UNIQUE NOT NULL,
	full_name     TEXT,
	username      TEXT,
	phone         TEXT,
	language      VARCHAR(2) NOT NULL DEFAULT 'uz' CHECK (language IN ('uz','ru')),
	is_active     BOOLEAN NOT NULL DEFAULT true,
	address       TEXT,
	abonent_id    VARCHAR(50),
	created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_clients_phone ON users(phone);

COMMIT;