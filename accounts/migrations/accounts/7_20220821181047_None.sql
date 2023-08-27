-- upgrade --
CREATE TABLE IF NOT EXISTS "accounts.user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(256),
    "last_name" VARCHAR(256),
    "username" VARCHAR(256) NOT NULL UNIQUE,
    "email" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(2048) NOT NULL,
    "type" VARCHAR(15) NOT NULL  DEFAULT 'normal'
);
COMMENT ON COLUMN "accounts.user"."type" IS 'NORMAL: normal\nORG: organization\nLEADER: leader';
CREATE TABLE IF NOT EXISTS "accounts.leader_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "phone_number" VARCHAR(32) NOT NULL,
    "avatar" VARCHAR(512),
    "city" VARCHAR(128) NOT NULL,
    "birth_date" DATE,
    "experience_level" INT NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "accounts.user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "accounts.normal_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "phone_number" VARCHAR(32) NOT NULL,
    "avatar" VARCHAR(512),
    "city" VARCHAR(128) NOT NULL,
    "birth_date" DATE,
    "user_id" INT NOT NULL UNIQUE REFERENCES "accounts.user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "accounts.org_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "phone_number" VARCHAR(32) NOT NULL,
    "avatar" VARCHAR(512),
    "city" VARCHAR(128) NOT NULL,
    "birth_date" DATE,
    "address" VARCHAR(256) NOT NULL,
    "certificate" VARCHAR(512) NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "accounts.user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "accounts.token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(128) NOT NULL UNIQUE,
    "user_id" INT NOT NULL UNIQUE REFERENCES "accounts.user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts.leader_profile_accounts.user" (
    "accounts.leader_profile_id" INT NOT NULL REFERENCES "accounts.leader_profile" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "accounts.user" ("id") ON DELETE CASCADE
);
