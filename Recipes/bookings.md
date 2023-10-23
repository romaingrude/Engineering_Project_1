# Single Table Design Recipe Template

_Copy this recipe template to design and create a database table from a specification._

## 1. Extract nouns from the user stories or specification

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

```
User: id, name, email, bookings
```

## 2. Infer the Table Name and Columns

Put the different nouns in this table. Replace the example with your own nouns.

| Record                | Properties                     |
| --------------------- | ------------------------------ |
| users                 | name, email, password          |


Name of the table (always plural): `albums`

Column names: `title`, `release_year`, `artist_id`

## 3. Decide the column types

[Here's a full documentation of PostgreSQL data types](https://www.postgresql.org/docs/current/datatype.html).

Most of the time, you'll need either `text`, `int`, `bigint`, `numeric`, or `boolean`. If you're in doubt, do some research or ask your peers.

Remember to **always** have the primary key `id` as a first column. Its type will always be `SERIAL`.

```
# EXAMPLE:

id: SERIAL
title: text
release_year: int
artist_id: int
```

## 4. Write the SQL

```sql
-- EXAMPLE
-- file: albums_table.sql

-- Replace the table name, columm names and types.

CREATE TABLE albums (
  id SERIAL PRIMARY KEY,
  title text,
  release_year int,
  artist_id int
);
```

## 5. Create the table

```bash
psql -h 127.0.0.1 database_name < albums_table.sql
```
