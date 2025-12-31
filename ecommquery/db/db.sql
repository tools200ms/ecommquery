
/* Redundant reference and property database

 */

CREATE TABLE prop_def (
    id CHAR(8) NOT NULL,
    ref_name varchar(255),
    type CHAR,
    validation_pattern varchar(255),
    flags CHAR, -- R: reference, P: property
    PRIMARY KEY (id)
);

-- Initialise dictionary ...

CREATE TABLE ns_def (
    id SMALLINT NOT NULL AUTO_INCREMENT,
    name CHAR(16),
    PRIMARY KEY (id),
    UNIQUE (id, name)
);

CREATE TABLE ns_prop_def (
    ns_id CHAR(8),
    prop_id SMALLINT,
    name VARCHAR(512),
    PRIMARY KEY (ns_id, prop_id),
    FOREIGN KEY (ns_id) REFERENCES ns_def(id),
    FOREIGN KEY (prop_id) REFERENCES prop_def(id)
);

-- CREATE TABLE ep_item_props (
--     id CHAR(16),
--     prop_id SMALLINT,
--     PRIMARY KEY (id, prop_id),
--     FOREIGN KEY (prop_id) REFERENCES item_prop_def(id)
-- );

-- END of definitions

-- CREATE TABLE set_def (
--     id SMALLINT NOT NULL AUTO_INCREMENT,
--     name CHAR(256),
--     ns_id SMALLINT,
--     PRIMARY KEY (id),
--     FOREIGN KEY (ns_id) REFERENCES ns_def(id),
--     UNIQUE (id, name)
-- );

CREATE TABLE set_prop_def (
    set_id SMALLINT,
    prop_id SMALLINT,
    --excl_prop_id SMALLINT,
    FOREIGN KEY (set_id) REFERENCES set_def(id),
    FOREIGN KEY (incl_prop_id) REFERENCES ns_prop_def(id),
    --FOREIGN KEY (excl_prop_id) REFERENCES ns_prop_def(id)
);

-- Object can be cloned into other set
CREATE TABLE obj (
    id INTEGER NOT NULL AUTO_INCREMENT,
    set_id SMALLINT,
    PRIMARY KEY (id, set_id),
    FOREIGN KEY (set_id) REFERENCES ns_prop_def(id),
);

CREATE TABLE obj_checkout_sources (
    id SMALLINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256),
    params VARCHAR(4096),
    PRIMARY KEY (id)
);

CREATE TABLE obj_checkout (
    id INTEGER NOT NULL AUTO_INCREMENT,
    obj_id INTEGER,
    from DATE NOT NULL,
    to DATE DEFAULT NULL,
    triggered_by SMALLINT,
    -- correction, transaction
    PRIMARY KEY (id),
    FOREIGN KEY (obj_id)
);

CREATE TABLE obj_prop_nochange (
    obj_id INTEGER,
    prop_id SMALLINT,
    checkout_id INTEGER,
    PRIMARY KEY (obj_id, prop_id),
    FOREIGN KEY (obj_id) REFERENCES obj(id),
    FOREIGN KEY (prop_id) REFERENCES set_prop_def(prop_id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

CREATE TABLE obj_prop_text (
    obj_id INTEGER,
    prop_id SMALLINT,
    checkout_id INTEGER,
    value VARCHAR(4096),
    PRIMARY KEY (obj_id, prop_id),
    FOREIGN KEY (obj_id) REFERENCES obj(id),
    FOREIGN KEY (prop_id) REFERENCES set_prop_def(prop_id),
    FOREIGN KEY (checkout_id) REFERENCES obj_checkout(id)
);

CREATE TABLE obj_prop_int (
    obj_id INTEGER,
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

