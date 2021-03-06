CREATE TABLE session_tb (
    id BIGSERIAL PRIMARY KEY,
    device_identifier VARCHAR NOT NULL,
	user_id BIGINT NOT NULL,
	initiated_at  TIMESTAMP NOT NULL,
	expires_at  TIMESTAMP NOT NULL,
	status VARCHAR NOT NULL DEFAULT 'ACTIVE',
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	idx BIGSERIAL,
	CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES user_tb(id) ON DELETE CASCADE
);
