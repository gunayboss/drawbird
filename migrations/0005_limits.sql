-- Fixed-window rate counters keyed by action + salted IP hash.
CREATE TABLE limits (
  k TEXT PRIMARY KEY,
  n INTEGER NOT NULL,
  exp INTEGER NOT NULL
);
