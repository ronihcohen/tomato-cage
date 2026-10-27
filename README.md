# Tomato cage

A fully 3D-printable triangular tomato cage (1.2 m tall, three rings) for a 5-gallon grow bag, modelled in build123d with [text-to-cad](https://github.com/earthtojake/text-to-cad).

## Parts per cage

| File | Qty | Print orientation |
|---|---|---|
| `pole_spike` | 3 | upright |
| `pole_segment` | 18 | upright |
| `pole_top` | 3 | upright |
| `corner_clip` | 9 | flat |
| `ring_bar` | 9 | lying flat |

All parts fit a Bambu A1 mini (180 × 180 × 180 mm). Print `ring_bar` diagonally on the plate (200 mm long).

Print files are in `STL/` and `3MF/`. PETG or ASA recommended for outdoor use.
`stake_connector` is a standalone sleeve for joining two 11 mm garden stakes.

## Assembly

1. Stack each pole: spike, 6 segments, top.
2. Push the poles into the bag in a triangle about 26 cm apart.
3. Snap 3 clips onto each pole (about 45, 80 and 115 cm up), open side facing out.
4. Push a bar between each pair of facing clips.

## Editing

Dimensions are constants at the top of `src/cage.py`. Rebuild with `cadgen run src/cage.py`; regenerate print files with `cd src && cadgen run exports.py`.
