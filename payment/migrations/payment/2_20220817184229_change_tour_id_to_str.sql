-- upgrade --
ALTER TABLE "payment.bill" ALTER COLUMN "tour_id" TYPE VARCHAR(64) USING "tour_id"::VARCHAR(64);
-- downgrade --
ALTER TABLE "payment.bill" ALTER COLUMN "tour_id" TYPE INT USING "tour_id"::INT;
