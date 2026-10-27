from cadgen import build123d as bd
from cadgen import stl, threemf


def sleeve_body(stake_d, clearance, wall, socket_depth, stop_len, stop_lip, chamfer):
    bore = stake_d + clearance
    outer = bore + 2 * wall
    length = 2 * socket_depth + stop_len

    body = bd.Cylinder(outer / 2, length)
    body = body - bd.Cylinder(bore / 2, length)
    # Internal stop ring in the middle so each stake seats at the same depth;
    # its underside is a 45-degree cone so it prints without supports
    ring = bd.Cylinder(bore / 2, stop_len) - bd.Cylinder(bore / 2 - stop_lip, stop_len)
    ring = ring - bd.Pos(0, 0, -stop_len / 2) * bd.Cone(
        bore / 2, bore / 2 - stop_lip, stop_lip, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    body = body + ring

    # Lead-in chamfers on both socket mouths
    mouths = body.edges().filter_by(bd.GeomType.CIRCLE).filter_by(
        lambda e: abs(e.radius - bore / 2) < 1e-6
        and abs(abs(e.center().Z) - length / 2) < 1e-6
    )
    body = bd.chamfer(mouths, chamfer)

    bb = body.bounding_box()
    assert abs(bb.size.X - outer) < 1e-3 and abs(bb.size.Z - length) < 1e-3

    body.label = "stake_connector"
    body.color = "#2e7d32"
    return body


@stl(out="../STL/stake_connector.stl")
@threemf(out="../3MF/stake_connector.3mf")
def stake_connector():
    # 11 mm stakes, 0.4 mm fit clearance for FDM printing
    return sleeve_body(stake_d=11, clearance=0.4, wall=2.5, socket_depth=30,
                       stop_len=3, stop_lip=1.5, chamfer=0.8)


if __name__ == "__main__":
    stake_connector()
