
CREATE TABLE Users (
    uid INTEGER,
    name VARCHAR(60),
    username VARCHAR(60),
    password VARCHAR(60),
    email TEXT,
    PRIMARY KEY(uid)
);

CREATE TABLE Representative (
    uid INTEGER,
    phone_number VARCHAR(60),
    zipcode INTEGER NOT NULL,
    FOREIGN KEY(zipcode) REFERENCES Zipcode,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
    PRIMARY KEY(uid),
);

CREATE TABLE Citizen (
    uid INTEGER,
    zipcode INTEGER NOT NULL,
    FOREIGN KEY(zipcode) REFERENCES Zipcode,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
    PRIMARY KEY(uid)
);

CREATE TABLE Zipcode (
    zipcode INTEGER,
    county TEXT,
    city_name TEXT
    PRIMARY KEY(zipcode)
);

CREATE TABLE Home (
    hid INTEGER,
    zipcode INTEGER, 
    FOREIGN KEY(zipcode) REFERENCES Zipcode,
    PRIMARY KEY(hid)
);

CREATE TABLE Score (
    amount INTEGER, 
    hid INTEGER,
    FOREIGN KEY(hid) REFERENCES Home,
    PRIMARY KEY(hid)
);

CREATE TABLE MoneyValue (
    year INTEGER,
    amount INTEGER,
    hid INTEGER,
    FOREIGN KEY(hid) REFERENCES Home,
    PRIMARY KEY(hid)
);

CREATE TABLE Topics (
    tid INTEGER,
    topic_name TEXT,
    UNIQUE(topic_name),
    PRIMARY KEY(tid)
);

CREATE TABLE Comments (
    comment TEXT,
    cid INTEGER,
    crid INTEGER,
    tid INTEGER,
    comid INTEGER,
    FOREIGN KEY(cid) REFERENCES Citizen ON DELETE CASCADE,
    FOREIGN KEY(crid) REFERENCES Critique ON DELETE CASCADE,
    FOREIGN KEY(tid) REFERENCES Topic ON DELETE CASCADE,
    PRIMARY KEY(comid)
);

CREATE TABLE Critique (
    total_pos INTEGER,
    total_neg INTEGER,
    crid INTEGER
    FOREIGN KEY(hid) REFERENCES Score,
    FOREIGN KEY(comid) REFERENCES Comments,
    PRIMARY KEY(crid)
);