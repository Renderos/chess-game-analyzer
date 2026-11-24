# Uso: python3 analyze.py partida.pgn moves.json [profundidad]
import chess, chess.pgn, chess.engine, io, json, math, sys, shutil
pgn = open(sys.argv[1]).read(); out_path = sys.argv[2]
depth = int(sys.argv[3]) if len(sys.argv) > 3 else 20
g = chess.pgn.read_game(io.StringIO(pgn)); b = g.board()
eng_path = shutil.which('stockfish') or '/usr/games/stockfish'
eng = chess.engine.SimpleEngine.popen_uci(eng_path); eng.configure({'Threads': 4, 'Hash': 256})
L = chess.engine.Limit(depth=depth)
V = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 0}
mat = lambda b: sum(V[p.piece_type] * (1 if p.color else -1) for p in b.piece_map().values())
wcp = lambda info: info['score'].white().score(mate_score=10000)
wp = lambda cp: 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)
info = eng.analyse(b, L); prev = wcp(info); best = info['pv'][0]
out = [{'fen': b.board_fen(), 'san': None, 'mat': 0, 'ev': prev}]
for m in g.mainline_moves():
    white = b.turn; san = b.san(m); bestsan = b.san(best); bestpv = b.variation_san(info['pv'][:5])
    frm, to = m.from_square, m.to_square
    b.push(m)
    if b.is_game_over():
        cur = (10000 if white else -10000) if b.is_checkmate() else 0
    else:
        info = eng.analyse(b, L); cur = wcp(info); best = info['pv'][0]
    s = 1 if white else -1
    out.append({'fen': b.board_fen(), 'san': san, 'from': chess.square_name(frm), 'to': chess.square_name(to),
                'mat': mat(b), 'check': b.is_check(), 'ev': cur, 'best': bestsan, 'bestpv': bestpv,
                'isbest': san == bestsan, 'loss': round(wp(prev * s) - wp(cur * s), 1), 'prev': prev})
    prev = cur
eng.quit()
json.dump(out, open(out_path, 'w'))
for i, o in enumerate(out[1:], 1):
    print(i, o['san'], 'ev', o['ev'], 'mejor', o['best'], 'pérdida', o['loss'], '|', o['bestpv'])
