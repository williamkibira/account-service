CREATE TABLE role_tb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_role_idx AFTER INSERT ON role_tb
		BEGIN
		    UPDATE role_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX role_tb_idx ON role_tb(idx);

CREATE TABLE user_tb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier VARCHAR(36) NOT NULL UNIQUE,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email_address VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_user_idx AFTER INSERT ON user_tb
		BEGIN
		    UPDATE user_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX user_tb_idx ON user_tb(idx);

CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_tb(id),
    CONSTRAINT fk_station FOREIGN KEY (role_id) REFERENCES role_tb(id)
);