# chess-game-analyzer

Skill para Claude que analiza partidas de ajedrez con **Stockfish** y genera una **página web animada** con:

- Tablero con piezas que se deslizan, barra y gráfica de evaluación
- Comentario en español para cada jugada
- Clasificación: teoría, gran jugada, mejor, excelente, buena, imprecisión, error, error grave
- Jugada preferida del motor y su línea principal
- Resumen de errores por jugador y claves de la partida

## Estructura

```
SKILL.md                 # Instrucciones de la skill (incluye scripts y plantilla embebidos)
scripts/analyze.py       # Análisis con Stockfish → moves.json
scripts/build.py         # Clasificación + comentarios → página HTML
scripts/template.html    # Plantilla de la página animada
examples/                # Ejemplo de salida
```

## Uso manual

```bash
pip install chess
sudo apt-get install stockfish
python3 scripts/analyze.py partida.pgn moves.json 20
# escribir notes.json y meta.json (ver SKILL.md)
python3 scripts/build.py moves.json notes.json meta.json scripts/template.html partida.html
```

## Uso como skill

Carga `SKILL.md` como skill en Claude y pega una partida en PGN: "analiza esta partida".

## Licencia

[MIT](LICENSE) © 2026 Ronald Ernesto Renderos Ramos
