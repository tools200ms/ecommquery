
-- CREATE VIEW obj_checkout_latest
--     AS SELECT id, max(timestamp) AS timestamp
--        FROM obj_checkout;


CREATE VIEW prop_int_latest
    AS SELECT pi.obj_id AS obj_id, pi.prop_id AS prop_id, max(timestamp) AS timestamp
        FROM obj_checkout c, obj_prop_int pi
        WHERE c.id = pi.checkout_id GROUP BY obj_id, prop_id, timestamp;


CREATE VIEW prop_text_latest
    AS SELECT pt.obj_id AS obj_id, pt.prop_id AS prop_id, max(timestamp) AS timestamp
        FROM obj_checkout c, obj_prop_text pt
        WHERE c.id = pt.checkout_id GROUP BY obj_id, prop_id, timestamp;
