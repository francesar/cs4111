CREATE TABLE Users (
    uid TEXT,
    name VARCHAR(60),
    username VARCHAR(60),
    password VARCHAR(60),
    email VARCHAR(60),
    zipcode VARCHAR(5) NOT NULL,
    hid TEXT NOT NULL,
    address TEXT,
    party_affiliation TEXT,
    FOREIGN KEY(zipcode) REFERENCES Zipcodes,
    FOREIGN KEY(hid) REFERENCES Homes,
    PRIMARY KEY(uid),
    CHECK (char_length(zipcode) = 5)
);

CREATE TABLE Representatives (
    uid TEXT NOT NULL,
    phone_number VARCHAR(60),
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Citizens (
    uid TEXT NOT NULL,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Homes (
    hid TEXT,
    score INTEGER,
    zipcode VARCHAR(5) NOT NULL,
    value INTEGER NOT NULL,
    CONSTRAINT valid_home_price CHECK(value > 0),
    FOREIGN KEY(zipcode) REFERENCES Zipcodes,
    PRIMARY KEY(hid)
);

CREATE TABLE Zipcodes (
    zipcode VARCHAR(5),
    county TEXT,
    city_name TEXT,
    avg_price INTEGER DEFAULT 0,
    CONSTRAINT valid_home_price CHECK(avg_price >= 0),
    CONSTRAINT valid_zip_length CHECK(char_length(zipcode) = 5),
    PRIMARY KEY(zipcode),
    CHECK (char_length(zipcode) = 5)
);

CREATE TABLE Topics (
    tid TEXT,
    topic_name TEXT,
    UNIQUE(topic_name),
    PRIMARY KEY(tid)
);

CREATE TABLE Comments (
    comment TEXT,
    uid TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    comment_id TEXT NOT NULL,
    sentiment INTEGER NOT NULL,
    zipcode VARCHAR(5) NOT NULL,
    date_posted TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY(zipcode) REFERENCES Zipcodes,
    FOREIGN KEY(topic_id) REFERENCES Topics ON DELETE CASCADE,
    PRIMARY KEY(comment_id)
);

CREATE TABLE Votes (
    vote_id TEXT,
    val INTEGER,
    comment_id TEXT,
    uid TEXT,
    FOREIGN KEY(comment_id) REFERENCES Comments,
    FOREIGN KEY(uid) REFERENCES Users,
    PRIMARY KEY(vote_id)
);

CREATE TABLE Representative_Comments (
    body TEXT,
    tokens TSVECTOR,
    cid TEXT NOT NULL,
    rid TEXT NOT NULL,
    document_id TEXT, 
    FOREIGN KEY(cid) REFERENCES Users,
    FOREIGN KEY(rid) REFERENCES Users,
    PRIMARY KEY(document_id)
);

/* adding column that contains the names of reps for a zipcode into an array */ 
ALTER TABLE zipcodes
ADD All_Reps text[]; 

-- Trigger Definition
-- CREATE FUNCTION parse_body() RETURNS trigger AS $parse_body$
--     BEGIN
--         IF NEW.body IS NULL THEN
--             RAISE EXCEPTION 'comment body cannot be null';
--         END IF;

--         -- Remember who changed the payroll when
--         NEW.tokens := to_tsvector(NEW.body);
--         RETURN NEW;
--     END;
-- $parse_body$ LANGUAGE plpgsql;


-- CREATE TRIGGER parse_body BEFORE INSERT OR UPDATE ON representative_comments
-- FOR EACH ROW EXECUTE PROCEDURE parse_body();