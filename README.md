# Tomato cage

A fully 3D-printable triangular tomato cage (1.2 m tall, three rings) for a 5-gallon grow bag, modelled in build123d with [text-to-cad](https://github.com/earthtojake/text-to-cad).

## Parts per cage

| File | Qty | Print orientation |
|---|---|---|
| `pole_spike` | 3 | upright, tip up (as exported) |
| `pole_segment` | 18 | upright |
| `pole_top` | 3 | upright, rounded end up |
| `pole_dowel` | 21 | upright |
| `corner_clip` | 9 | flat, raised arms up |
| `ring_bar` | 9 | lying flat |

All parts fit a Bambu A1 mini (180 × 180 × 180 mm) and print without supports in the orientations above.
A brim helps the tall, thin pole pieces stay put.

Print files are in `STL/` and `3MF/`. PETG or ASA recommended for outdoor use.

## Assembly

1. Stack each pole: spike, 6 segments, top, with a dowel in every joint.
2. Push the poles into the bag in a triangle about 23 cm apart.
3. Snap 3 clips onto each pole (about 45, 80 and 115 cm up), open side facing out.
4. Push a bar between each pair of facing clips.

## Editing

Dimensions are constants at the top of `src/cage.py`. Rebuild the print files and `STEP/cage.step` with `python src/cage.py`, run through cadgen's Python: `uvx --from cadgen==0.7.26 python src/cage.py`.
