CREATE TABLE IF NOT EXISTS subreddits (
    id_subreddit TEXT NOT NULL COLLATE NOCASE,
    name TEXT,
    display_name TEXT,
    description TEXT,
    over_18 BOOLEAN,
    last_scraped INTEGER,
    last_submission_scraped TEXT,
    PRIMARY KEY(id_subreddit)
);

CREATE TABLE IF NOT EXISTS  redditors (
    id_redditor TEXT COLLATE NOCASE,
    name TEXT,
    has_verified_mail BOOLEAN,
    created_utc INTEGER,
    bad_record BOOLEAN,
    PRIMARY KEY(id_redditor)
);

CREATE TABLE IF NOT EXISTS  submissions (
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

CREATE TABLE IF NOT EXISTS  comments (
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

CREATE TABLE IF NOT EXISTS  category (
    id_submission TEXT,
    id_comment TEXT,
    cat TEXT,
    cnt INTEGER
);

CREATE INDEX IF NOT EXISTS  category_id_submission_IDX ON category (id_submission);
CREATE INDEX IF NOT EXISTS  category_id_comment_IDX ON category (id_id_comment);


-- submissions definition

CREATE TABLE IF NOT EXISTS  submissions (
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

