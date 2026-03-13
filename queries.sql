SELECT id, name FROM users;
SELECT id;
SELECT FROM users;
SELECT id FROM;
SELECT * FROM users WHERE age > 18;
SELECT * users;
SELECT id FROM users WHERE;

SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
SELECT name FROM users WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);
SELECT * FROM users WHERE id = (SELECT MAX(id) FROM users);
SELECT * FROM users WHERE id IN (SELECT);
SELECT * FROM users WHERE id IN SELECT user_id FROM orders;
SELECT * FROM users WHERE id IN (SELECT user_id orders);
SELECT * FROM users WHERE id = (SELECT FROM users);

CREATE TABLE users (id INT, name VARCHAR(100));
CREATE users (id INT);
CREATE TABLE (id INT);
CREATE TABLE users ();
CREATE TABLE users (id);

INSERT INTO users (id, name) VALUES (1, 'John');
INSERT users (id, name) VALUES (1, 'John');
INSERT INTO users (id, name);
INSERT INTO users (id, name) VALUES (1);
INSERT INTO users VALUES (1, 'John');

INSERT INTO users (id, name) SELECT id, name FROM temp_users;
INSERT INTO users SELECT id FROM temp_users;
INSERT INTO users (id, name) SELECT FROM temp_users;
INSERT INTO users (id) SELECT id, name FROM temp_users;

DELETE FROM users WHERE id = 1;
DELETE users WHERE id = 1;
DELETE FROM WHERE id = 1;
DELETE FROM users WHERE;

DELETE FROM users WHERE id IN (SELECT user_id FROM orders);
DELETE FROM users WHERE id IN (SELECT);
DELETE FROM users WHERE id IN SELECT user_id FROM orders;
DELETE FROM users WHERE id = (SELECT FROM users);

DROP TABLE users;
DROP users;
DROP TABLE;
DROP TABLE users NOW;

ALTER TABLE users ADD age INT;
ALTER users ADD age INT;
ALTER TABLE ADD age INT;
ALTER TABLE users ADD age;
ALTER TABLE users MODIFY;
ALTER TABLE users ADD last_login DATE;
ALTER TABLE users DROP COLUMN age;
ALTER TABLE users ADD (age INT);
ALTER TABLE users ADD age;
