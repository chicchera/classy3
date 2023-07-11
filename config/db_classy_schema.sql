-- new tables
CREATE TABLE "subreddits" (
	"id_subreddit"	TEXT NOT NULL COLLATE NOCASE,
	"name"	TEXT,
	"display_name"	TEXT,
	"description"	TEXT,
	"over_18"	BOOLEAN,
	"last_scraped"	INTEGER,
	"last_submission_scraped"	TEXT,
	PRIMARY KEY("id_subreddit")
)

CREATE TABLE "redditors" (
	"id_redditor"	TEXT COLLATE NOCASE,
	"name"	TEXT,
	"has_verified_mail"	BOOLEAN,
	"created_utc"	INTEGER,
	"bad_record"	BOOLEAN,
	PRIMARY KEY("id_redditor")
)

CREATE TABLE "submissions" (
	"id_submission"	TEXT UNIQUE COLLATE NOCASE,
	"id_author"	TEXT COLLATE NOCASE,
	"id_subreddit"	TEXT COLLATE NOCASE,
	"title"	TEXT,
	"body"	TEXT,
	"score"	INTEGER,
	"over_18"	BOOLEAN,
	"ama"	BOOLEAN,
	"serio"	BOOLEAN,
	"tonto_index"	INTEGER,
	"created_utc"	INTEGER,
	PRIMARY KEY("id_submission")
)

CREATE TABLE "comments_2" (
	"id_comment"	TEXT NOT NULL COLLATE NOCASE,
	"id_submission"	TEXT COLLATE NOCASE,
	"id_parent"	TEXT COLLATE NOCASE,
	"body"	TEXT,
	"is_submitter"	BOOLEAN,
	"score"	INTEGER,
	"created_utc"	INTEGER,
	PRIMARY KEY("id_comment")
)
-- category definition

CREATE TABLE "category" (
    "rid_post"  TEXT,
    "rid_comment"   TEXT,
    "cat"   TEXT,
    "cnt"   INTEGER
);

CREATE INDEX category_rid_post_IDX ON category (rid_post);
CREATE INDEX category_rid_comment_IDX ON category (rid_comment);


-- comments definition

CREATE TABLE "comments" (
    "body" TEXT COLLATE NOCASE,
    "dfrid_comment" INTEGER,
    "rid_comment" TEXT,
    "dfrid_post" INTEGER,
    "rid_post" TEXT,
    "dfrid_parent" INTEGER,
    "rid_parent" TEXT,
    "dfrid_author" INTEGER,
    "rid_author" TEXT,
    "score" INTEGER,
    "date_posted" INTEGER,
    "is_op" INTEGER
);

CREATE INDEX comments_rid_comment_IDX ON comments (rid_comment);
CREATE INDEX comments_dfrid_IDX ON comments (dfrid_comment);
CREATE INDEX comments_dfrid_author_IDX ON comments (dfrid_author,is_op);
CREATE INDEX comments_rid_post_IDX ON comments (rid_post);


-- ids definition

CREATE TABLE "ids" (
    "tbl" TEXT,       /* (P)ost (C)omment (U)ser (S)ubreddit */
    "id_dfr" INTEGER, /* the id as in the dfr database */
    "id_red" TEXT     /* the is in reddit format (text) */
);

CREATE INDEX ids_id_dfr_IDX ON ids (id_dfr);
CREATE INDEX ids_id_red_IDX ON ids (id_red);
CREATE INDEX ids_id_dfr_tbl_IDX ON ids (id_dfr, tbl);
CREATE INDEX ids_id_red_tbl_IDX ON ids (id_red, tbl);


-- objects definition

CREATE TABLE "objects" (
    "dfrid_object" INTEGER,
    "rid_object" TEXT COLLATE NOCASE,
    "tbl" TEXT,
    "name" TEXT COLLATE NOCASE,
    "created" TIMESTAMP,
    "has_mail" BOOLEAN,
    "bad_rec" BOOLEAN DEFAULT False,
    "sub_enabled" BOOLEAN DEFAULT False,
    "gender" TEXT
);

CREATE INDEX "objects_rid_red_IDX" ON "objects" ("id_red");
CREATE INDEX "objects_dfrid_object_IDX" ON "objects" ("dfrid_object");
CREATE INDEX "objects_tbl_IDX" ON "objects" ("tbl","name");
CREATE INDEX "objects_name_IDX" ON "objects" ("name");


-- submissions definition

CREATE TABLE "submissions" (
	"id_submission"	TEXT UNIQUE COLLATE NOCASE,
	"id_author"	TEXT COLLATE NOCASE,
	"id_subreddit"	TEXT COLLATE NOCASE,
	"title"	TEXT,
	"body"	TEXT,
	"score"	INTEGER,
	"over_18"	BOOLEAN,
	"ama"	BOOLEAN,
	"serio"	BOOLEAN,
	"tonto_index"	INTEGER,
	"created_utc"	INTEGER,
	PRIMARY KEY("id_submission")
)





-- cats_base definition

CREATE TABLE "cats_base" (
    "rid_post" TEXT,
    "rid_comment" TEXT,
    "tbl" TEXT,                 /* (N)o sw, (U)nique no stowords, (L)emmas - based on N, (l)emmas - based on (L) */
    "title" TEXT COLLATE NOCASE,
    "body" TEXT COLLATE NOCASE
);

CREATE INDEX "cats_base_rid_post_IDX" ON "cats_base" ("rid_post");
CREATE INDEX "cats_base_rid_comment_IDX" ON "cats_base" ("rid_comment");
CREATE INDEX "cats_base_rid_post_tbl_IDX" ON "cats_base" ("rid_post", "tbl");
CREATE INDEX "cats_base_rid_comment_tbl_DX" ON "cats_base" ("rid_comment", "tbl");
CREATE INDEX "cats_base_rid_post_comments_IDX" ON "cats_base" ("rid_post","rid_comment", "tbl");

-- sort_base definition. Replaces cats_base

CREATE TABLE "sort_base" (
	"rid_post"	TEXT,
	"rid_comment"	TEXT,
	"qa"	TEXT NOT NULL,
	"code"	TEXT NOT NULL,
	"content"	TEXT COLLATE NOCASE,
	UNIQUE("rid_post","rid_comment","qa","code")
)

CREATE INDEX "sort_base_rid_post_IDX" ON "sort_base" ("rid_post");
CREATE INDEX "sort_base_rid_comment_IDX" ON "sort_base" ("rid_comment");
CREATE INDEX "sort_base_rid_post_code_IDX" ON "sort_base" ("rid_post", "code");
CREATE INDEX "sort_base_rid_comment_code_DX" ON "sort_base" ("rid_comment", "code");
CREATE INDEX "sort_base_rid_post_comments_IDX" ON "sort_base" ("rid_post","rid_comment", "code");
/*
CREATE UNIQUE INDEX "sort_base_unique_IDX" ON "sort_base" (
	"rid_post",
	"rid_comment",
	"code",
	"qa"
)
*/

-- enum definition, used for decoding codes

CREATE TABLE "enum" (
	"id"	INTEGER NOT NULL UNIQUE,
	"code"	TEXT NOT NULL UNIQUE,
	"des"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO enum (code,des) VALUES
	 ('NS','NoSw_Dups'),
	 ('ND','NoSw_NoDups'),
	 ('LD','Lemma_Dups'),
	 ('SD','Stemma_Dups');

-- view to select q & a to tokenize

CREATE VIEW vw_to_tokenize
AS
SELECT
    rid_post,
    rid_comment,
    code,
    qa,
    content
FROM (
    SELECT
        p1.rid_post,
        NULL AS rid_comment,
        'NS' AS code,
        'Q' AS qa,
        rtrim(coalesce(p1.title || ' ', '') || coalesce(p1.body, '')) AS content
    FROM
        posts AS p1
    UNION ALL
    SELECT
        p2.rid_post,
        NULL AS rid_comment,
        'ND' AS code,
        'Q' AS qa,
        rtrim(coalesce(p2.title || ' ', '') || coalesce(p2.body, '')) AS content
    FROM
        posts AS p2
    UNION ALL
    SELECT
        p3.rid_post,
        NULL AS rid_comment,
        'LD' AS code,
        'Q' AS qa,
        rtrim(coalesce(p3.title || ' ', '') || coalesce(p3.body, '')) AS content
    FROM
        posts AS p3
    UNION ALL
    SELECT
        p4.rid_post,
        NULL AS rid_comment,
        'SD' AS code,
        'Q' AS qa,
        rtrim(coalesce(p4.title || ' ', '') || coalesce(p4.body, '')) AS content
    FROM
        posts AS p4
    UNION ALL
    SELECT
        c1.rid_post,
        c1.rid_comment,
        'NS' AS code,
        'A' AS qa,
        body AS content
    FROM
        comments AS c1
    UNION ALL
    SELECT
        c2.rid_post,
        c2.rid_comment,
        'NS' AS code,
        'A' AS qa,
        body AS content
    FROM
        comments AS c2
    UNION ALL
    SELECT
        c3.rid_post,
        c3.rid_comment,
        'LD' AS code,
        'A' AS qa,
        body AS content
    FROM
        comments AS c3
    UNION ALL
    SELECT
        c4.rid_post,
        c4.rid_comment,
        'SD' AS code,
        'A' AS qa,
        body AS content
    FROM
        comments AS c4
)
WHERE rid_post NOT IN (
	SELECT rid_post FROM sort_base)
AND rid_comment NOT IN (
	SELECT rid_comment FROM sort_base)
AND code NOT IN (
	SELECT code FROM sort_base)
AND qa NOT IN (
	SELECT qa FROM sort_base);


"""
CREATE TEMPORARY TABLE row_data AS
SELECT
    p1.rid_post,
    NULL AS rid_comment,
    'NS' AS code,
    'Q' AS qa,
    rtrim(coalesce(p1.title || ' ', '') || coalesce(p1.body, '')) AS content
FROM
    posts p1
UNION ALL
SELECT
    p2.rid_post,
    NULL AS rid_comment,
    'ND' AS code,
    'Q' AS qa,
    rtrim(coalesce(p2.title || ' ', '') || coalesce(p2.body, '')) AS content
FROM
    posts p2
UNION ALL
SELECT
    p3.rid_post,
    NULL AS rid_comment,
    'LD' AS code,
    'Q' AS qa,
    rtrim(coalesce(p3.title || ' ', '') || coalesce(p3.body, '')) AS content
FROM
    posts p3
UNION ALL
SELECT
    p4.rid_post,
    NULL AS rid_comment,
    'SD' AS code,
    'Q' AS qa,
    rtrim(coalesce(p4.title || ' ', '') || coalesce(p4.body, '')) AS content
FROM
    posts p4
UNION ALL
SELECT
    c1.rid_post,
    c1.rid_comment,
    'NS' AS code,
    'A' AS qa,
    body AS content
FROM
    comments c1
UNION ALL
SELECT
    c2.rid_post,
    c2.rid_comment,
    'NS' AS code,
    'A' AS qa,
    body AS content
FROM
    comments c2
UNION ALL
SELECT
    c3.rid_post,
    c3.rid_comment,
    'LD' AS code,
    'A' AS qa,
    body AS content
FROM
    comments c3
UNION ALL
SELECT
    c4.rid_post,
    c4.rid_comment,
    'SD' AS code,
    'A' AS qa,
    body AS content
FROM
    comments c4;



DELETE FROM sort_base
WHERE ....

"""
