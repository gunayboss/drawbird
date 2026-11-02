-- Per-IP daily count of newly created identities; only a salted hash of the IP, kept two days.
CREATE TABLE new_ids (
  day TEXT NOT NULL,
  ip_hash TEXT NOT NULL,
  n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, ip_hash)
);
