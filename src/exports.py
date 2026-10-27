"""Writes the print files for every cage part."""
from cage import corner_clip, pole_segment, pole_spike, pole_top, ring_bar

if __name__ == "__main__":
    for part in (pole_spike, pole_segment, pole_top, corner_clip, ring_bar):
        part().export(f"../STL/{part.__name__}.stl", f"../3MF/{part.__name__}.3mf")
