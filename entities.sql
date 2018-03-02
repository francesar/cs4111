CREATE TABLE Users (
    uid INTEGER,
    name VARCHAR(60),
    username VARCHAR(60),
    password VARCHAR(60),
    email TEXT,
    zipcode VARCHAR(5) NOT NULL
    FOREIGN KEY(zipcode) REFERENCES Zipcode
    PRIMARY KEY(uid)
    CHECK (char_length(zipcode) == 5)
);

CREATE TABLE Representative (
    uid INTEGER NOT NULL,
    phone_number VARCHAR(60),
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
);

CREATE TABLE Citizen (
    uid INTEGER NOT NULL,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Home (
    hid INTEGER,
    score INTEGER,
    zipcode INTEGER NOT NULL, 
    FOREIGN KEY(zipcode) REFERENCES Zipcode,
    PRIMARY KEY(hid, zipcode)
);

CREATE TABLE Zipcode (
    zipcode VARCHAR(5) NOT NULL,
    county TEXT,
    city_name TEXT
    PRIMARY KEY(zipcode)
    CHECK (char_length(zipcode) == 5)
);

CREATE TABLE Score (
    amount INTEGER, 
    hid INTEGER NOT NULL,
    FOREIGN KEY(hid) REFERENCES Home,
    PRIMARY KEY(hid)
);

CREATE TABLE MoneyValue (
    year INTEGER,
    amount INTEGER,
    hid INTEGER,
    FOREIGN KEY(hid) REFERENCES Home,
    PRIMARY KEY(hid)
    CHECK (amount > 0 AND year > 1970)
);

CREATE TABLE Topics (
    tid INTEGER,
    topic_name TEXT,
    UNIQUE(topic_name),
    PRIMARY KEY(tid)
);

CREATE TABLE Comments (
    comment TEXT,
    cid INTEGER NOT NULL,
    tid INTEGER NOT NULL,
    comid INTEGER NOT NULL,
    FOREIGN KEY(cid) REFERENCES Citizen ON DELETE CASCADE,
    FOREIGN KEY(tid) REFERENCES Topic ON DELETE CASCADE,
    PRIMARY KEY(comid)
);