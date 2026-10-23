"""Export two DaS samples as compact OpenGL camera trajectories for the site.

Usage:
    python tools/export_showcase.py --samples PATH/TO/das_package/samples

Each sample's pose_variants/tkcam.npy contains world-to-camera matrices in the
DaS basis. sample.json records the conversion from relative OpenGL camera-to-
world poses: conjugate by B = diag(1, -1, -1), then invert. We undo that
conversion here. The original 12D model outputs are not part of these local
samples, so we recover per-frame velocities from the converted positions and
integrate them again to verify that the exported path matches the poses.
"""

import argparse
import json
from pathlib import Path

import numpy as np


EXAMPLES = {
    "000952": "Approaching the house",
    "000596": "Revealing the bedroom",
}
BASIS = np.diag([1.0, -1.0, -1.0, 1.0])


def export_sample(root: Path, sample_id: str, title: str) -> dict:
    folder = root / sample_id
    metadata = json.loads((folder / "sample.json").read_text(encoding="utf-8"))
    assert metadata["pose_variants"]["tkcam"]["layout"] == "world_to_camera_homogeneous"
    poses_das = np.load(folder / "pose_variants" / "tkcam.npy").astype(np.float64)
    assert poses_das.ndim == 3 and poses_das.shape[1:] == (4, 4)

    poses_gl = BASIS @ np.linalg.inv(poses_das) @ BASIS
    poses_gl = np.linalg.inv(poses_gl[0]) @ poses_gl
    positions = poses_gl[:, :3, 3]
    rotations = poses_gl[:, :3, :3]

    # The 12D feature layout is [xyz, dxyz, rotation col 1, rotation col 2].
    velocity = np.zeros_like(positions)
    velocity[1:] = np.diff(positions, axis=0)
    velocity[0] = velocity[1]
    integrated = np.zeros_like(positions)
    integrated[0] = positions[0]
    integrated[1:] = integrated[0] + np.cumsum(velocity[1:], axis=0)
    assert np.max(np.abs(integrated - positions)) < 1e-5
    assert np.max(np.abs(rotations @ rotations.transpose(0, 2, 1) - np.eye(3))) < 1e-4
    assert np.min(np.linalg.det(rotations)) > 0.999

    frames = []
    for position, rotation in zip(integrated, rotations):
        right = rotation[:, 0]
        up = rotation[:, 1]
        frames.append([round(float(value), 6) for value in (*position, *right, *up)])

    return {
        "id": sample_id,
        "title": title,
        "prompt": metadata["prompt"],
        "frames": frames,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "static/data/showcase.json",
    )
    args = parser.parse_args()
    data = {
        "coordinate_system": "relative OpenGL camera-to-world; +X right, +Y up, -Z forward",
        "frame_format": "[x,y,z,right_x,right_y,right_z,up_x,up_y,up_z]",
        "examples": [export_sample(args.samples, sample_id, title) for sample_id, title in EXAMPLES.items()],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    for example in data["examples"]:
        end = example["frames"][-1][:3]
        print(f"{example['id']}: {len(example['frames'])} frames, end position {end}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
