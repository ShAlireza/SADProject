-- upgrade --
CREATE TABLE IF NOT EXISTS "payment.bill" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "tour_id" INT NOT NULL,
    "reserve_count" INT NOT NULL  DEFAULT 1,
    "item_cost" DOUBLE PRECISION NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 2
);
COMMENT ON COLUMN "payment.bill"."item_cost" IS 'Per item(tour) cost';
COMMENT ON COLUMN "payment.bill"."status" IS 'PAYED: 0\nFAILED: 1\nPENDING: 2';;
CREATE TABLE IF NOT EXISTS "payment.zarinpal_payment_request" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(512) NOT NULL  DEFAULT 'Alantouring tour payment',
    "authority" VARCHAR(128),
    "ref_id" VARCHAR(64),
    "bill_id" INT NOT NULL REFERENCES "payment.bill" ("id") ON DELETE CASCADE
);-- downgrade --
DROP TABLE IF EXISTS "payment.bill";
DROP TABLE IF EXISTS "payment.zarinpal_payment_request";
