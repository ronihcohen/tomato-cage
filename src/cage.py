"""Fully printable triangular tomato cage: three segmented poles, three rings.

Every part fits a Bambu A1 mini (180 mm cube); the 200 mm bars print diagonally. Poles plug together peg-into-socket;
corner clips snap onto the poles and hold square bars that form each ring.
"""
import math

import build123d as bd
from cadgen import model

POLE_D = 14          # pole diameter
PEG_D = 8            # pole joint peg
PEG_LEN = 15
FIT = 0.4            # print clearance on every fit
SEG_LEN = 150        # pole segment length (without peg); pieces stay under 180 mm
SPIKE_LEN = 40       # pointed tip on the bottom segment

BAR = 10             # square ring-bar section
BAR_LEN = 200

CLIP_H = 16          # clip height and arm section
CLIP_OD = 21
CLIP_OPENING = 11.5  # snap-on gap, narrower than the pole
CLIP_GRIP = 0.3      # clip bore smaller than the pole so it clamps in place
BAR_FIT = 0.2        # snug bar sockets
SOCKET_START = 14    # socket floor, measured from the pole axis
SOCKET_DEPTH = 16

# Pole spacing follows from the bar length and the clip sockets
SIDE = BAR_LEN + 2 * SOCKET_START + 2 * 0.5
RING_HEIGHTS = (450, 800, 1150)
GREEN = "#2e7d32"


def pole_body(kind):
    body = bd.Cylinder(POLE_D / 2, SEG_LEN, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    if kind == "spike":
        body = body - bd.Cylinder(POLE_D, SPIKE_LEN, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        body = body + bd.Cone(1.5, POLE_D / 2, SPIKE_LEN, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    else:
        socket = bd.Cylinder((PEG_D + FIT) / 2, PEG_LEN + 1,
                             align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        body = body - socket
    if kind == "top":
        top_edge = body.edges().filter_by(bd.GeomType.CIRCLE).sort_by(bd.Axis.Z)[-1]
        body = bd.fillet(top_edge, 4)
    else:
        peg = bd.Pos(0, 0, SEG_LEN) * bd.Cylinder(PEG_D / 2, PEG_LEN, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        peg = bd.chamfer(peg.edges().sort_by(bd.Axis.Z)[-1], 0.8)
        body = body + peg
    return body


@model
def pole_spike():
    body = pole_body("spike")
    assert abs(body.bounding_box().size.Z - (SEG_LEN + PEG_LEN)) < 1e-3
    body.label, body.color = "pole_spike", GREEN
    return body


@model
def pole_segment():
    body = pole_body("segment")
    assert abs(body.bounding_box().size.Z - (SEG_LEN + PEG_LEN)) < 1e-3
    body.label, body.color = "pole_segment", GREEN
    return body


@model
def pole_top():
    body = pole_body("top")
    assert abs(body.bounding_box().size.Z - SEG_LEN) < 1e-3
    body.label, body.color = "pole_top", GREEN
    return body


@model
def corner_clip():
    reach = SOCKET_START + SOCKET_DEPTH
    collar = bd.Cylinder(CLIP_OD / 2, CLIP_H)
    body = collar
    # Two arms 60 degrees apart, both facing the cage centre (local -X)
    for angle in (150, 210):
        arm = bd.Pos(reach / 2, 0, 0) * bd.Box(reach, CLIP_H, CLIP_H)
        socket = bd.Pos(SOCKET_START + SOCKET_DEPTH / 2 + 0.5, 0, 0) * bd.Box(
            SOCKET_DEPTH + 1, BAR + BAR_FIT, BAR + BAR_FIT)
        body = body + bd.Rot(Z=angle) * arm
        body = body - bd.Rot(Z=angle) * socket
    body = body - bd.Cylinder((POLE_D - CLIP_GRIP) / 2, CLIP_H)
    # Snap-on opening on the outside of the pole
    body = body - bd.Pos(CLIP_OD / 2, 0, 0) * bd.Box(CLIP_OD, CLIP_OPENING, CLIP_H)
    assert abs(body.bounding_box().size.Z - CLIP_H) < 1e-3
    body.label, body.color = "corner_clip", "#66bb6a"
    return body


@model
def ring_bar():
    body = bd.Box(BAR_LEN, BAR, BAR)
    long_edges = body.edges().filter_by(bd.Axis.X)
    body = bd.chamfer(long_edges, 1)
    assert abs(body.bounding_box().size.X - BAR_LEN) < 1e-3
    body.label, body.color = "ring_bar", "#81c784"
    return body


@model
def cage():
    spike, seg, top = pole_spike().shape, pole_segment().shape, pole_top().shape
    clip, bar = corner_clip().shape, ring_bar().shape
    radius = SIDE / math.sqrt(3)
    angles = (90, 210, 330)
    corners = [(radius * math.cos(math.radians(a)), radius * math.sin(math.radians(a))) for a in angles]

    parts = []
    for i, (a, (x, y)) in enumerate(zip(angles, corners)):
        stack = [spike] + [seg] * 6 + [top]
        for k, piece in enumerate(stack):
            p = bd.Pos(x, y, k * SEG_LEN) * piece
            p.label, p.color = f"pole{i + 1}_{piece.label}_{k}", GREEN
            parts.append(p)
        for h in RING_HEIGHTS:
            c = bd.Pos(x, y, h) * bd.Rot(Z=a) * clip
            c.label, c.color = f"clip_p{i + 1}_{h}", clip.color
            parts.append(c)

    for i in range(3):
        (x1, y1), (x2, y2) = corners[i], corners[(i + 1) % 3]
        heading = math.degrees(math.atan2(y2 - y1, x2 - x1))
        for h in RING_HEIGHTS:
            b = bd.Pos((x1 + x2) / 2, (y1 + y2) / 2, h) * bd.Rot(Z=heading) * bar
            b.label, b.color = f"bar_s{i + 1}_{h}", bar.color
            parts.append(b)

    assembly = bd.Compound(children=parts)
    assembly.label = "cage"
    return assembly


if __name__ == "__main__":
    cage()
