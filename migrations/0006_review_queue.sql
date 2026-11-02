-- New birds from new artists wait for review; artists become trusted after 2 approved birds.
ALTER TABLE birds ADD COLUMN status TEXT NOT NULL DEFAULT 'live';
ALTER TABLE users ADD COLUMN trusted INTEGER NOT NULL DEFAULT 0;
-- Stable salted hash of the IP the artist last posted from, used only to make bans stick.
ALTER TABLE users ADD COLUMN ip_hash TEXT;
CREATE INDEX birds_status ON birds(status);

UPDATE users SET trusted = 1 WHERE uid IN (SELECT uid FROM birds GROUP BY uid HAVING COUNT(*) >= 2);

CREATE TABLE ip_bans (
  ip_hash TEXT PRIMARY KEY,
  exp INTEGER NOT NULL
);

CREATE TABLE settings (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL
);
