# USERS

_Copy this recipe template to design and create a database table from a specification._

## Extract nouns from the user stories or specification

```

Any signed-up user can list a new space.
Users can list multiple spaces.
Users should be able to name their space, provide a short description of the space, and a price per night.
Users should be able to offer a range of dates where their space is available.
Any signed-up user can request to hire any space for one night, and this should be approved by the user that owns that space.
Nights for which a space has already been booked should not be available for users to book that space.
Until a user has confirmed a booking request, that space can still be booked for that night.


EXCALIDRAW
- Name
- Email
- Password
- Bookings


User: id, name, email, bookings
```

## Infer the Table Name and Columns

Put the different nouns in this table. Replace the example with your own nouns.

| Record                | Properties                     |
| --------------------- | ------------------------------ |
| users                 | name, email, password          |


## Decide the column types


```
# EXAMPLE:

id: SERIAL
name: text
email: text
password: text
```

## 4. Write the SQL

```sql
-- EXAMPLE
-- file: albums_table.sql

-- Replace the table name, columm names and types.

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name text,
  email text,
  password text
);
```

## 5. Create the table

```bash
psql -h 127.0.0.1 database_name < albums_table.sql
```


# ROOMS

_Copy this recipe template to design and create a database table from a specification._

## Extract nouns from the user stories or specification

```

Any signed-up user can list a new space.
Users can list multiple spaces.
Users should be able to name their space, provide a short description of the space, and a price per night.
Users should be able to offer a range of dates where their space is available.
Any signed-up user can request to hire any space for one night, and this should be approved by the user that owns that space.
Nights for which a space has already been booked should not be available for users to book that space.
Until a user has confirmed a booking request, that space can still be booked for that night.



```

## Infer the Table Name and Columns

Put the different nouns in this table. Replace the example with your own nouns.

| Record                | Properties                                |
| --------------------- | ---------------------------------         |
| rooms                 | name, price, description, user_id         |


## Decide the column types


```
# EXAMPLE:

id: SERIAL
name: text
price: float
description: text
```

## 4. Write the SQL

```sql
-- EXAMPLE
-- file: albums_table.sql

-- Replace the table name, columm names and types.

CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  name text,
  price float,
  description text,
  booking_start date,
  booking_end date,
  user_id int,
  constraint fk_user foreign key(user_id)
    references users(id)
    on delete cascade
);
```

## 5. Create the table

```bash
psql -h 127.0.0.1 database_name < albums_table.sql
```

# BOOKINGS

_Copy this recipe template to design and create a database table from a specification._

## Extract nouns from the user stories or specification

```

Any signed-up user can list a new space.
Users can list multiple spaces.
Users should be able to name their space, provide a short description of the space, and a price per night.
Users should be able to offer a range of dates where their space is available.
Any signed-up user can request to hire any space for one night, and this should be approved by the user that owns that space.
Nights for which a space has already been booked should not be available for users to book that space.
Until a user has confirmed a booking request, that space can still be booked for that night.



```

## Infer the Table Name and Columns

Put the different nouns in this table. Replace the example with your own nouns.

| Record                | Properties                                   |
| --------------------- | ---------------------------------            |
| bookings              | room_id, user_id, confirmation, booking_start, booking_end |


## Decide the column types


```
# EXAMPLE:

id: SERIAL
name: text
price: float
description: text
```

## 4. Write the SQL

```sql
-- EXAMPLE
-- file: albums_table.sql

-- Replace the table name, columm names and types.

CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  name text,
  price float,
  description text,
  booking_start date,
  booking_end date,
  user_id int,
  constraint fk_user foreign key(user_id)
    references users(id)
    on delete cascade
);
```

## 5. Create the table

```bash
psql -h 127.0.0.1 database_name < albums_table.sql
```
