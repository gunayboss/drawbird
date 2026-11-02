CREATE TABLE users (
  uid TEXT PRIMARY KEY,
  token_hash TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL DEFAULT '',
  created INTEGER NOT NULL
);

CREATE TABLE birds (
  id TEXT PRIMARY KEY,
  uid TEXT NOT NULL REFERENCES users(uid),
  name TEXT NOT NULL,
  img TEXT NOT NULL,
  created INTEGER NOT NULL,
  ai_score INTEGER,
  ai_bird INTEGER
);
CREATE INDEX birds_uid ON birds(uid);

CREATE TABLE votes (
  uid TEXT NOT NULL,
  bird_id TEXT NOT NULL,
  v INTEGER NOT NULL CHECK (v IN (-1, 1)),
  PRIMARY KEY (uid, bird_id)
);
CREATE INDEX votes_bird ON votes(bird_id);

CREATE TABLE flags (
  uid TEXT NOT NULL,
  bird_id TEXT NOT NULL,
  PRIMARY KEY (uid, bird_id)
);

CREATE TABLE flocks (
  id TEXT PRIMARY KEY,
  uid TEXT NOT NULL,
  name TEXT NOT NULL,
  birds TEXT NOT NULL DEFAULT '[]',
  created INTEGER NOT NULL
);
CREATE INDEX flocks_uid ON flocks(uid);
