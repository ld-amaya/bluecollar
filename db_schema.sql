CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "first_name" string(50),
  "last_name" string(50),
  "facebook" string(100),
  "email" string(50),
  "password" text,
  "mobile" int,
  "apartment_number" string(5),
  "building" string(50),
  "street" string(50),
  "city_id" int,
  "barangay_id" int
);

CREATE TABLE "city" (
  "id" SERIAL PRIMARY KEY,
  "name" string(50),
  "user_id" int
);

CREATE TABLE "barangay" (
  "id" SERIAL PRIMARY KEY,
  "name" string(50),
  "city_id" int,
  "user_id" int
);

CREATE TABLE "type" (
  "id" SERIAL PRIMARY KEY,
  "name" string
);

CREATE TABLE "user_type" (
  "int" SERIAL PRIMARY KEY,
  "user_id" int,
  "type_id" int
);

CREATE TABLE "job" (
  "id" SERIAL PRIMARY KEY,
  "job" string(50),
  "description" text
);

CREATE TABLE "user_job" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "job_id" int
);

CREATE TABLE "job_type" (
  "id" SERIAL PRIMARY KEY,
  "name" string(50)
);

CREATE TABLE "user_job_type" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "job_type_id" int
);

CREATE TABLE "comment" (
  "id" SERIAL PRIMARY KEY,
  "comment" text,
  "user_from" int,
  "user_to" int
);

CREATE TABLE "rating" (
  "id" SERIAL PRIMARY KEY,
  "rating" int,
  "user_from" int,
  "user_to" int
);

CREATE TABLE "message" (
  "id" SERIAL PRIMARY KEY,
  "message" text
);

CREATE TABLE "user_message" (
  "id" SERIAL PRIMARY KEY,
  "message_id" int,
  "message_from" int,
  "message_to" int
);

ALTER TABLE "type" ADD FOREIGN KEY ("id") REFERENCES "user_type" ("type_id");

ALTER TABLE "user_type" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "rating" ADD FOREIGN KEY ("user_from") REFERENCES "users" ("id");

ALTER TABLE "rating" ADD FOREIGN KEY ("user_to") REFERENCES "users" ("id");

ALTER TABLE "comment" ADD FOREIGN KEY ("user_from") REFERENCES "users" ("id");

ALTER TABLE "comment" ADD FOREIGN KEY ("user_to") REFERENCES "users" ("id");

ALTER TABLE "user_message" ADD FOREIGN KEY ("message_id") REFERENCES "message" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "user_message" ("message_from");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "user_message" ("message_to");

ALTER TABLE "user_job" ADD FOREIGN KEY ("job_id") REFERENCES "job_type" ("id");

ALTER TABLE "user_job" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "job" ADD FOREIGN KEY ("id") REFERENCES "users" ("id");

ALTER TABLE "user_job_type" ADD FOREIGN KEY ("job_type_id") REFERENCES "job" ("id");

ALTER TABLE "user_job_type" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "city" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "barangay" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "barangay" ADD FOREIGN KEY ("city_id") REFERENCES "city" ("id");
