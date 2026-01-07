
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    msg VARCHAR(4096),
    msg_date DATETIME DEFAULT (datetime('now', 'localtime'))
);

INSERT INTO comments (msg)
    VALUES ('Database has been created');


-- Initialise dictionary ...

DROP TABLE IF EXISTS spc_def;
CREATE TABLE spc_def (
    id SMALLINT PRIMARY KEY,
    name CHAR(16),
    UNIQUE (id, name)
);

DROP TABLE IF EXISTS part_def;
CREATE TABLE part_def (
    id SMALLINT PRIMARY KEY,
    spc_id SMALLINT NOT NULL,
    name CHAR(64),
    FOREIGN KEY (spc_id) REFERENCES spc_def(id),
    UNIQUE (id, spc_id, name)
);

DROP TABLE IF EXISTS prop_def;
CREATE TABLE prop_def (
    id SMALLINT PRIMARY KEY,
    spc_id CHAR(8) DEFAULT NULL,
    ref_name varchar(255),
    type CHAR,
    validator_fun varchar(255),
    flags CHAR, -- R: reference, P: property
    FOREIGN KEY (spc_id) REFERENCES spc_def(id)
);
-- EAN
-- Name
-- Detailed name


DROP TABLE IF EXISTS checkout_sources_def;
CREATE TABLE checkout_sources_def (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(256),
    part_id SMALLINT NOT NULL,
    function VARCHAR,
    triggered_by SMALLINT DEFAULT NULL,
    FOREIGN KEY (part_id) REFERENCES part_def(id)
);

-- END of definitions

DROP TABLE IF EXISTS obj_checkout;
CREATE TABLE obj_checkout (
    id INTEGER PRIMARY KEY,
    --part_id SMALLINT,
    --obj_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
    --till DATETIME DEFAULT NULL,
    src_id SMALLINT,
    -- correction, transaction
    -- PRIMARY KEY (id, obj_id),
    FOREIGN KEY (src_id) REFERENCES checkout_sources_def(id)
);

DROP TABLE IF EXISTS obj_prop_nochange;
CREATE TABLE obj_prop_nochange (
    prop_id SMALLINT,
    checkout_id INTEGER,
    UNIQUE (prop_id, checkout_id),
    FOREIGN KEY (prop_id) REFERENCES prop_def(id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

DROP TABLE IF EXISTS obj_prop_text;
CREATE TABLE obj_prop_text (
    prop_id SMALLINT,
    checkout_id INTEGER,
    value CHAR(32),
    UNIQUE (prop_id, checkout_id),
    FOREIGN KEY (prop_id) REFERENCES prop_def(id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

DROP TABLE IF EXISTS obj_prop_int;
CREATE TABLE obj_prop_int (
    prop_id SMALLINT,
    checkout_id INTEGER,
    value INTEGER,
    UNIQUE (prop_id, checkout_id),
    FOREIGN KEY (prop_id) REFERENCES prop_def(id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

-- Partitions for historical objects

-- # short name
-- # descriptive name
-- # EAN
-- # Offer ID
-- transaction, accurate transaction, ref, validated
-- updte, accurate time -

