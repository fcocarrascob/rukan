"""Presencia de este archivo en la raíz: pytest agrega la raíz del repo a
`sys.path`, y con eso `lab` y `lab._lib` se importan sin instalar nada.

Los scripts del laboratorio se corren con `python -m lab.notaNN_slug` desde la
raíz, que hace lo mismo. `verification/` no lo necesita: sus casos solo importan
`rukan`, que sí está instalado (`pip install -e .`).
"""
