
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

CREATE VIEW obj_int_latest
    AS SELECT alli.obj_id AS obj_id, alli.prop_id AS prop_id, latesti.timestamp AS timestamp, alli.checkout_id AS checkout_id, alli.value as value
        FROM prop_int_latest latesti, obj_prop_int alli
        WHERE latesti.prop_id = alli.prop_id AND latesti.obj_id = alli.obj_id;

CREATE VIEW obj_text_latest
    AS SELECT allt.obj_id AS obj_id, allt.prop_id AS prop_id, latestt.timestamp AS timestamp, allt.checkout_id AS checkout_id, allt.value as value
        FROM prop_text_latest latestt, obj_prop_text allt
        WHERE latestt.prop_id = allt.prop_id AND latestt.obj_id = allt.obj_id;

CREATE VIEW obj_comb_latest
    AS SELECT obj_id, prop_def.spc_id, prop_def.ref_name AS ref_name, checkout_id, obj_text_latest.value AS valuet, obj_int_latest.value AS valuei, oc.timestamp AS timestamp
        FROM obj_text_latest FULL OUTER JOIN obj_int_latest USING (checkout_id, obj_id, prop_id), obj_checkout oc, prop_def
        WHERE oc.id = checkout_id AND prop_def.id = prop_id;

CREATE VIEW _obj_comb_latest
    AS SELECT obj_id, prop_id, checkout_id, obj_text_latest.value AS valuet, obj_int_latest.value AS valuei
        FROM obj_text_latest FULL OUTER JOIN obj_int_latest USING (checkout_id, obj_id, prop_id), obj_checkout oc
        WHERE oc.id = checkout_id;
