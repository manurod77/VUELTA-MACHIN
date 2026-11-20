#!/usr/bin/env python3
"""Genera las ediciones de Clave Circular desde una fuente única.
   core.tpl = código común. editions/*.patch = lo que cambia cada edición respecto al núcleo.
   {{N}} = número de versión de la edición (editions.json). Uso: python3 src/build.py [--check]"""
import json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cfg = json.load(open(os.path.join(HERE, "editions.json"), encoding="utf-8"))
core = os.path.join(HERE, "core.tpl")
ok = True
for name, c in cfg.items():
    tmp = tempfile.mkdtemp(); work = os.path.join(tmp, "f.tpl"); shutil.copy(core, work)
    if c.get("patch"):
        r = subprocess.run(["patch", "--no-backup-if-mismatch", "-F0", "-s", work, os.path.join(HERE, c["patch"])], capture_output=True, text=True)
        if r.returncode != 0:
            print("FALLA el parche de", name, "\n", r.stdout, r.stderr); ok = False; continue
    out = open(work, encoding="utf-8", newline="").read().replace("{{N}}", c["version"])
    if "<meta charset" not in out[:2048]:
        out = '<meta charset="utf-8">\n' + out   # sin esto, al abrir el archivo suelto algunos navegadores muestran mal los acentos
    dest = os.path.join(ROOT, c["out"])
    if "--check" in sys.argv:
        same = os.path.exists(dest) and open(dest, encoding="utf-8", newline="").read() == out
        print(("IGUAL   " if same else "DIFIERE ") + name); ok = ok and same
    else:
        open(dest, "w", encoding="utf-8", newline="").write(out); print("generado", c["out"])
sys.exit(0 if ok else 1)
