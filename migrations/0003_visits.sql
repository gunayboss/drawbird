-- Cookieless daily visit counter: one row per UTC day, no visitor data.
CREATE TABLE visits (
  day TEXT PRIMARY KEY,
  n INTEGER NOT NULL DEFAULT 0
);
