-- "Bize yaz" contact form: reports, KVKK requests, bugs, ideas. Deleted a year after they arrive.
CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  uid TEXT,
  topic TEXT NOT NULL,
  body TEXT NOT NULL,
  contact TEXT NOT NULL DEFAULT '',
  created INTEGER NOT NULL,
  done INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX messages_created ON messages(created);
