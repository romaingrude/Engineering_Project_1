-- USERS TABLE
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_seq CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name text,
    email text,
    password text
);

INSERT INTO users (name, email, password) VALUES ('John', 'test@gmail.com', '1234');
INSERT INTO users (name, email, password) VALUES ('Jane', 'test2@gmail.com', '1234');


-- ROOMS TABLE
DROP TABLE IF EXISTS rooms CASCADE;
DROP SEQUENCE IF EXISTS rooms_seq CASCADE;

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name text,
    price float,
    description text,
    user_id int,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE
);

INSERT INTO rooms (name, price, description, user_id) VALUES ('Room 1', 100, 'This is a room', 1);
INSERT INTO rooms (name, price, description, user_id) VALUES ('Room 2', 200, 'This is another room', 2);

-- BOOKINGS TABLE
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_seq;

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id int,
    room_id int,
    confirmation boolean,
    booking_start date,
    booking_end date,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE,
    CONSTRAINT fk_room FOREIGN KEY (room_id)
    REFERENCES rooms (id)
    ON DELETE CASCADE
);

INSERT INTO bookings (user_id, room_id, confirmation, booking_start, booking_end) VALUES (1, 1, true, '2021-01-01', '2021-01-02');
INSERT INTO bookings (user_id, room_id, confirmation, booking_start, booking_end) VALUES (2, 2, true, '2021-01-01', '2021-01-02');