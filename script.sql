CREATE TABLE week(
    day_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    day_name TEXT
);

CREATE TABLE subject(
    subj_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subj_name TEXT
);

CREATE TABLE lesson(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT,
    day_id INTEGER,
    les_num INTEGER,
    subj_id INTEGER,
    room TEXT,
    time_start TEXT,
    time_end TEXT,
    FOREIGN KEY (subj_id) REFERENCES subject(subj_id) ON DELETE SET NULL,
    FOREIGN KEY (day_id) REFERENCES week(day_id) ON DELETE SET NULL
);