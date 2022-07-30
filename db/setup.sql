CREATE TABLE if not exists vehicle(
    vin text PRIMARY KEY NOT NULL,
    make text,
    model text,
    model_year text,
    body_class text
);