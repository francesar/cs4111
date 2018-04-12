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
