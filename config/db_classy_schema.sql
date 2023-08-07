-- category definition

CREATE TABLE category (
    id_submission TEXT,
    id_comment TEXT,
    cat TEXT,
    cnt INTEGER
);

CREATE INDEX "category_id_comment_idx" ON "category" (
	"id_comment"
);
CREATE INDEX "category_id_submission_idx" ON "category" (
	"id_submission"
);


-- comments definition

CREATE TABLE "comments" (
	"id_comment"	TEXT NOT NULL UNIQUE COLLATE NOCASE,
	"id_submission"	TEXT COLLATE NOCASE,
	"id_parent"	TEXT COLLATE NOCASE,
	"id_redditor"	TEXT COLLATE NOCASE,
	"body"	TEXT,
	"is_submitter"	BOOLEAN,
	"score"	INTEGER,
	"created_utc"	INTEGER,
	PRIMARY KEY("id_comment")
);

CREATE INDEX "comments_created_DESC_utc_idx" ON "comments" (
	"created_utc"	DESC
);
CREATE INDEX "comments_created_utc_idx" ON "comments" (
	"created_utc"
);
CREATE INDEX "comments_id_comment_idx" ON "comments" (
	"id_comment"
);
CREATE INDEX "comments_id_redditor_idx" ON "comments" (
	"id_redditor"
);
CREATE INDEX "comments_id_submission_idx" ON "comments" (
	"id_submission"
);


-- redditors definition

CREATE TABLE "redditors" (
	"id_redditor"	TEXT COLLATE NOCASE,
	"redditor"	TEXT UNIQUE COLLATE NOCASE,
	"has_verified_email"	BOOLEAN,
	"created_utc"	INTEGER,
	"bad_record"	BOOLEAN,
	PRIMARY KEY("redditor")
);

CREATE INDEX redditors_created_utc_idx ON redditors (created_utc);
CREATE INDEX redditors_created_utc_DESC_idx ON redditors (created_utc DESC);


-- submissions definition

CREATE TABLE "submissions" (
	"id_submission"	TEXT NOT NULL UNIQUE COLLATE NOCASE,
	"id_redditor"	TEXT DEFAULT 000 COLLATE NOCASE,
	"id_subreddit"	TEXT COLLATE NOCASE,
	"title"	TEXT,
	"body"	TEXT,
	"redditor"	TEXT,
	"score"	INTEGER,
	"over_18"	BOOLEAN,
	"ama"	BOOLEAN,
	"serio"	BOOLEAN,
	"tonto_index"	INTEGER,
	"created_utc"	INTEGER,
	"subreddit"	TEXT,
	PRIMARY KEY("id_submission")
);

CREATE INDEX "submissions_created_utc_DESC_idx" ON "submissions" (
	"created_utc"	DESC
);
CREATE INDEX "submissions_created_utc_idx" ON "submissions" (
	"created_utc"
);
CREATE INDEX "submissions_id_redditor_idx" ON "submissions" (
	"id_redditor"
);
CREATE INDEX "submissions_id_submissions_idx" ON "submissions" (
	"id_submission"
);
CREATE INDEX "submissions_id_subreddit_idx" ON "submissions" (
	"id_subreddit"
);


-- subreddits definition

CREATE TABLE "subreddits" (
	"id_subreddit"	TEXT COLLATE NOCASE,
	"name"	TEXT NOT NULL UNIQUE COLLATE NOCASE,
	"created_utc"	INTEGER,
	"display_name"	TEXT,
	"description"	TEXT,
	"over_18"	BOOLEAN,
	"last_submission_id"	TEXT,
	"last_submission_utc"	INTEGER,
	"last_scraped_utc"	INTEGER,
	PRIMARY KEY("name")
);