-- constants definition

CREATE TABLE IF NOT EXISTS  "constants" (
	"tbl"	TEXT COLLATE NOCASE,
	"code"	TEXT COLLATE NOCASE,
	"des"	TEXT COLLATE NOCASE,
	UNIQUE ("tbl","code")
);
-- Prefixes
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', '', 'Submission');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't1_', 'Comment');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't2_', 'Account');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't3_', 'Link');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't4_', 'Message');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't5_', 'Subreddit');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('type_prefixes', 't6_', 'Award');

-- txt_transform codes
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'OT', 'Orginal_Title');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'OB', 'Original_Body');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'TN', 'Original_Title_Punctuation_Correctd');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'BN', 'Original_Body_Punctuation_Correctd');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'PD', 'Poll_data');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'TT', 'Title_normalized');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'BB', 'Body_Normalized');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'SP', 'Misspells');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'NS', 'No_Stopwords');
INSERT OR IGNORE INTO constants
(tbl, code, des)
VALUES('transforms', 'SS', 'Single_Stopwords');

-- redditors definition

CREATE TABLE IF NOT EXISTS "redditors" (
    "id_redditor"   TEXT COLLATE NOCASE,
    "redditor"  TEXT UNIQUE COLLATE NOCASE,
    "has_verified_email"    BOOLEAN,
    "created_utc"   INTEGER,
    "bad_record"    BOOLEAN,
    PRIMARY KEY("redditor")
);

CREATE INDEX IF NOT EXISTS redditors_created_utc_idx ON redditors (created_utc);
CREATE INDEX IF NOT EXISTS redditors_created_utc_DESC_idx ON redditors (created_utc DESC);


-- submissions definition

CREATE TABLE IF NOT EXISTS "submissions" (
    "id_submission" TEXT NOT NULL UNIQUE COLLATE NOCASE,
    "id_redditor"   TEXT DEFAULT 000 COLLATE NOCASE,
    "id_subreddit"  TEXT COLLATE NOCASE,
    "redditor"  TEXT,
    "score" INTEGER,
    "over_18"   BOOLEAN DEFAULT 0,
    "ama"   BOOLEAN DEFAULT 0,
    "serio" BOOLEAN DEFAULT 0,
    "is_poll" BOOLEAN DEFAULT 0,
    "tonto_index"   INTEGER,
    "created_utc"   INTEGER,
    "subreddit" TEXT,
    "num_comments"  INTEGER,
    "upvote_ratio"  NUMERIC,
    "view_count"    INTEGER,
    "ups"   INTEGER,
    "downs" INTEGER,
    "locked"    BOOLEAN DEFAULT 0,
    "archived"  BOOLEAN DEFAULT 0,
    PRIMARY KEY("id_submission")
);

CREATE INDEX IF NOT EXISTS "submissions_created_utc_DESC_idx" ON "submissions" (
    "created_utc"   DESC
);
CREATE INDEX IF NOT EXISTS "submissions_created_utc_idx" ON "submissions" (
    "created_utc"
);
CREATE INDEX IF NOT EXISTS "submissions_id_redditor_idx" ON "submissions" (
    "id_redditor"
);
CREATE INDEX IF NOT EXISTS "submissions_id_submissions_idx" ON "submissions" (
    "id_submission"
);
CREATE INDEX IF NOT EXISTS "submissions_id_subreddit_idx" ON "submissions" (
    "id_subreddit"
);

-- subreddits definition

CREATE TABLE IF NOT EXISTS "subreddits" (
    "id_subreddit"  TEXT COLLATE NOCASE,
    "name"  TEXT NOT NULL UNIQUE COLLATE NOCASE,
    "created_utc"   INTEGER,
    "display_name"  TEXT,
    "description"   TEXT,
    "over_18"   BOOLEAN,
    "last_submission_id"    TEXT,
    "last_submission_utc"   INTEGER,
    "last_scraped_utc"  INTEGER,
    PRIMARY KEY("name")
);


-- comments definition

CREATE TABLE IF NOT EXISTS comments (
    id_comment TEXT,
    id_submission TEXT,
    id_parent TEXT,
    id_redditor TEXT,
    body TEXT,
    is_submitter BOOLEAN,
    score INTEGER,
    created_utc INTEGER,
    CONSTRAINT COMMENTS_PK PRIMARY KEY (id_comment),
    CONSTRAINT comments_FK FOREIGN KEY (id_submission) REFERENCES submissions(id_submission) ON DELETE CASCADE
);


-- txt_transforms definition

CREATE TABLE IF NOT EXISTS "txt_transforms" (
    "id_submission" TEXT,
    "id_comment"    TEXT,
    "kind"  TEXT,
    "content"   TEXT,
    CONSTRAINT "category_FK" FOREIGN KEY("id_submission") REFERENCES "submissions"("id_submission") ON DELETE CASCADE,
    CONSTRAINT "category_FK2" FOREIGN KEY("id_comment") REFERENCES "comments"("id_comment") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_submission_comment" ON "txt_transforms" (
    "id_submission",
    "id_comment"
);
CREATE INDEX IF NOT EXISTS "idx_submission_comment_kind" ON "txt_transforms" (
    "id_submission",
    "id_comment",
    "kind"
);



-- category definition

CREATE TABLE IF NOT EXISTS "category" (
    "id_submission" TEXT,
    "id_comment"    TEXT,
    "cat"   TEXT,
    "cnt"   INTEGER,
    CONSTRAINT "category_FK" FOREIGN KEY("id_submission") REFERENCES "submissions"("id_submission") ON DELETE CASCADE,
    CONSTRAINT "category_FK2" FOREIGN KEY("id_comment") REFERENCES "comments"("id_comment") ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_category_cat_cnt ON category (cat, cnt);

CREATE TABLE "indexes" (
	"id_submission"	TEXT,
	"id_comment"	TEXT,
	"kind"	TEXT,
    "letters"	INTEGER DEFAULT NULL,
	"paragraphs"	INTEGER DEFAULT NULL,
	"sentences"	INTEGER DEFAULT NULL,
	"syllables"	INTEGER DEFAULT NULL,
	"num_words"	INTEGER DEFAULT NULL,
	"distinct_words"	INTEGER DEFAULT NULL,
	"unique_words"	INTEGER DEFAULT NULL,
	"misspells"	INTEGER DEFAULT NULL,
	"enthropy"	NUMBER DEFAULT NULL,
	"redundancy"	NUMBER DEFAULT NULL,
	"density"	NUMBER DEFAULT NULL
);
CREATE INDEX "indexes_full_key_idx" ON "indexes" (
	"id_submission",
	"id_comment",
	"kind"
);