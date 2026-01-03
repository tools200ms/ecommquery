

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    msg VARCHAR(4096),
    msg_date DATETIME DEFAULT (datetime('now', 'localtime'))
);

INSERT INTO comments (msg)
    VALUES ('Database has been created');


-- Initialise dictionary ...

DROP TABLE IF EXISTS ns_def;
CREATE TABLE ns_def (
    id SMALLINT NOT NULL,
    name CHAR(16),
    PRIMARY KEY (id),
    UNIQUE (id, name)
);

DROP TABLE IF EXISTS part_def;
CREATE TABLE part_def {
    id SMALLINT NOT NULL,
    spc_id SMALLINT,
    name CHAR(16),
    PRIMARY KEY (id),
    UNIQUE (id, spc_id, name)
}

DROP TABLE IF EXISTS prop_def;
CREATE TABLE prop_def (
    id CHAR(8) NOT NULL,
    ns_id CHAR(8) DEFAULT NULL,
    ref_name varchar(255),
    type CHAR,
    validation_pattern varchar(255),
    flags CHAR, -- R: reference, P: property
    PRIMARY KEY (id)
);
-- EAN
-- Name
-- Detailed name

--DROP TABLE IF EXISTS ns_prop_def;
--CREATE TABLE ns_prop_def (
--    ns_id CHAR(8),
--    prop_id SMALLINT,
--    name VARCHAR(512),
--    PRIMARY KEY (ns_id, prop_id),
--    UNIQUE prop_id,
--    FOREIGN KEY (ns_id) REFERENCES ns_def(id),
--    FOREIGN KEY (prop_id) REFERENCES prop_def(id)
--);
-- ProdID (Presta)
-- OferID (Allegro)


-- END of definitions


--DROP TABLE IF EXISTS part_prop_def;
--CREATE TABLE part_prop_def (
--    part_id SMALLINT,
--    prop_id SMALLINT,
--    --excl_prop_id SMALLINT,
--    FOREIGN KEY (part_id) REFERENCES part_def(id),
--    FOREIGN KEY (prop_id) REFERENCES ns_prop_def(id)
--    --FOREIGN KEY (excl_prop_id) REFERENCES ns_prop_def(id)
--);

-- Object can be cloned into other set
--DROP TABLE IF EXISTS obj;
--CREATE TABLE obj (
--    id INTEGER NOT NULL,
--    --part_id SMALLINT,
--    PRIMARY KEY (id),
--    --FOREIGN KEY (part_id) REFERENCES ns_prop_def(id)
--);

DROP TABLE IF EXISTS checkout_sources_def;
CREATE TABLE obj_checkout_sources (
    id SMALLINT NOT NULL,
    name VARCHAR(256),
    part_id_scope SMALLINT NOT NULL,
    function VARCHAR,
    triggered_by SMALLINT DEFAULT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS obj_checkout;
CREATE TABLE obj_checkout (
    id INTEGER NOT NULL,
    --part_id SMALLINT,
    obj_id INTEGER NOT NULL,
    on DATETIME DEFAULT (datetime('now', 'localtime')),
    --till DATETIME DEFAULT NULL,
    triggered_by SMALLINT,
    -- correction, transaction
    PRIMARY KEY (id, obj_id)
    --FOREIGN KEY (obj_id) REFERENCES obj(id)
);

DROP TABLE IF EXISTS obj_prop_nochange;
CREATE TABLE obj_prop_nochange (
    --obj_id INTEGER,
    prop_id SMALLINT,
    checkout_id INTEGER,
    PRIMARY KEY (obj_id, prop_id),
    FOREIGN KEY (obj_id) REFERENCES obj(id),
    FOREIGN KEY (prop_id) REFERENCES part_prop_def(prop_id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

DROP TABLE IF EXISTS obj_prop_text;
CREATE TABLE obj_prop_text (
    --obj_id INTEGER,
    prop_id SMALLINT,
    checkout_id INTEGER,
    value VARCHAR(4096),
    PRIMARY KEY (obj_id, prop_id),
    FOREIGN KEY (obj_id) REFERENCES obj(id),
    FOREIGN KEY (prop_id) REFERENCES part_prop_def(prop_id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

DROP TABLE IF EXISTS obj_prop_int;
CREATE TABLE obj_prop_int (
    --obj_id INTEGER,
    prop_id SMALLINT,
    checkout_id INTEGER,
    value INTEGER,
    PRIMARY KEY (obj_id, prop_id),
    FOREIGN KEY (obj_id) REFERENCES obj(id),
    FOREIGN KEY (prop_id) REFERENCES ns_prop_def(id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

-- Partitions for historical objects

-- # short name
-- # descriptive name
-- # EAN
-- # Offer ID
-- transaction, accurate transaction, ref, validated
-- updte, accurate time -

