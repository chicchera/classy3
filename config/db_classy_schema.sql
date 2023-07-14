CREATE TABLE subreddits (
    id_subreddit TEXT NOT NULL COLLATE NOCASE,
    name TEXT,
    display_name TEXT,
    description TEXT,
    over_18 BOOLEAN,
    last_scraped INTEGER,
    last_submission_scraped TEXT,
    PRIMARY KEY(id_subreddit)
);

CREATE TABLE redditors (
    id_redditor TEXT COLLATE NOCASE,
    name TEXT,
    has_verified_mail BOOLEAN,
    created_utc INTEGER,
    bad_record BOOLEAN,
    PRIMARY KEY(id_redditor)
);

CREATE TABLE submissions (
    id_submission TEXT UNIQUE COLLATE NOCASE,
    id_redditor TEXT COLLATE NOCASE,
    id_subreddit TEXT COLLATE NOCASE,
    title TEXT,
    body TEXT,
    score INTEGER,
    over_18 BOOLEAN,
    ama BOOLEAN,
    serio BOOLEAN,
    tonto_index INTEGER,
    created_utc INTEGER,
    PRIMARY KEY(id_submission)
);

CREATE TABLE comments (
    id_comment TEXT NOT NULL COLLATE NOCASE,
    id_submission TEXT COLLATE NOCASE,
    id_parent TEXT COLLATE NOCASE,
    body TEXT,
    is_submitter BOOLEAN,
    score INTEGER,
    created_utc INTEGER,
    PRIMARY KEY(id_comment)
);
-- category definition

CREATE TABLE category (
    id_submission TEXT,
    id_comment TEXT,
    cat TEXT,
    cnt INTEGER
);

CREATE INDEX category_id_submission_IDX ON category (id_submission);
CREATE INDEX category_id_comment_IDX ON category (id_id_comment);


-- submissions definition

CREATE TABLE submissions (
    id_submission TEXT UNIQUE COLLATE NOCASE,
    id_redditor TEXT COLLATE NOCASE,
    id_subreddit TEXT COLLATE NOCASE,
    title TEXT,
    body TEXT,
    score INTEGER,
    over_18 BOOLEAN,
    ama BOOLEAN,
    serio BOOLEAN,
    tonto_index INTEGER,
    created_utc INTEGER,
    PRIMARY KEY(id_submission)
);

