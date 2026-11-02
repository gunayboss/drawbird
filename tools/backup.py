"""Backs up the live D1 database to a dated .sql file and keeps the newest 12.

Run from the project root:  python tools/backup.py [target folder]
Default folder: DRAWBIRD_BACKUP_DIR, or ~/drawbird-yedek. Keep backups out of the repo: they contain user data.
Restore (overwrites!):  npx wrangler d1 execute drawbird --remote --file <backup.sql>
"""
import datetime, glob, os, subprocess, sys

KEEP = 12
target = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('DRAWBIRD_BACKUP_DIR', os.path.join(os.path.expanduser('~'), 'drawbird-yedek'))
os.makedirs(target, exist_ok=True)
out = os.path.join(target, f'drawbird-{datetime.date.today().isoformat()}.sql')
root = os.path.join(os.path.dirname(__file__), '..')
cmd = ['npx', 'wrangler', 'd1', 'export', 'drawbird', '--remote', '--output', out]
r = subprocess.run(cmd, cwd=root, shell=os.name == 'nt')
if r.returncode != 0 or not os.path.exists(out):
    sys.exit('Yedek alınamadı. `npx wrangler login` ile giriş yaptığından emin ol.')
for old in sorted(glob.glob(os.path.join(target, 'drawbird-*.sql')))[:-KEEP]:
    os.remove(old)
print(f'Yedek hazır: {out} ({os.path.getsize(out) // 1024} KB)')
