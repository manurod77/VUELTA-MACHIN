# Fuente única de Clave Circular

- `core.tpl`: código común a todas las ediciones. Los cambios generales se hacen aquí, una sola vez.
- `editions/*.patch`: lo que cambia cada edición respecto al núcleo (marca, tema, escenas, kits propios).
- `editions.json`: salida y número de versión de cada edición. `{{N}}` en el código = esa versión.
- `python3 src/build.py` regenera `index.html`, `dark-empaths/index.html` y `vanilla/index.html`.
- `python3 src/build.py --check` comprueba que los archivos publicados coinciden con lo generado.
- Si un parche no aplica (el cambio al núcleo tocó una zona que la edición también modifica), el build falla y lo dice.
