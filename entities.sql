CREATE TABLE Users (
    uid INTEGER,
    name VARCHAR(60),
    username VARCHAR(60),
    password VARCHAR(60),
    email VARCHAR(60),
    zipcode VARCHAR(5) NOT NULL,
    hid INTEGER NOT NULL,
    FOREIGN KEY(zipcode) REFERENCES Zipcodes,
    FOREIGN KEY(hid) REFERENCES Home,
    PRIMARY KEY(uid),
    CHECK (char_length(zipcode) == 5)
);

CREATE TABLE Representatives (
    uid INTEGER NOT NULL,
    phone_number VARCHAR(60),
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Citizens (
    uid INTEGER NOT NULL,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Homes (
    hid INTEGER,
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
    avg_zillow_price INTEGER,
    CONSTRAINT valid_home_price CHECK(avg_zillow_price > 0),
    CONSTRAINT valid_zip_length CHECK(char_length(zipcode) = 5),
    PRIMARY KEY(zipcode)
    CHECK (char_length(zipcode) == 5)
);

CREATE TABLE Topics (
    tid INTEGER,
    topic_name TEXT,
    UNIQUE(topic_name),
    PRIMARY KEY(tid)
);

CREATE TABLE Comments (
    comment TEXT,
    uid INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    sentiment INTEGER NOT NULL,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY(topic_id) REFERENCES Topics ON DELETE CASCADE,
    PRIMARY KEY(comment_id)
);

CREATE TABLE Votes (
    vote_id INTEGER,
    val INTEGER,
    comment_id INTEGER,
    uid INTEGER,
    FOREIGN KEY(comment_id) REFERENCES Comments,
    FOREIGN KEY(uid) REFERENCES Users,
    PRIMARY KEY(vote_id)
);

SELECT AVG(H.value)
FROM homes H
WHERE H.zipcode = '60651';

SELECT U.zipcode, COUNT(U.name) as AmountOfReps
FROM users U NATURAL JOIN representatives R 
GROUP BY U.zipcode

SELECT C.topic_id, COUNT(*) 
FROM comments C NATURAL JOIN users U 
GROUP BY C.topic_id;
