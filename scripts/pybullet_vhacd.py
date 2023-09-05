""" Script for approximate convex decomposition """
# global
import typing
import json
import time
import argparse
import jsbeautifier
import pybullet as p
from pathlib import Path
from pybullet_utils.bullet_client import BulletClient

# typing
SeqType = typing.Sequence


def drawAABB(bullet_client: BulletClient, aabb: SeqType[SeqType[float]]) -> None:
    aabbMin = aabb[0]
    aabbMax = aabb[1]
    f = [aabbMin[0], aabbMin[1], aabbMin[2]]
    t = [aabbMax[0], aabbMin[1], aabbMin[2]]
    bullet_client.addUserDebugLine(f, t, [1, 0, 0])
    f = [aabbMin[0], aabbMin[1], aabbMin[2]]
    t = [aabbMin[0], aabbMax[1], aabbMin[2]]
    bullet_client.addUserDebugLine(f, t, [0, 1, 0])
    f = [aabbMin[0], aabbMin[1], aabbMin[2]]
    t = [aabbMin[0], aabbMin[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [0, 0, 1])

    f = [aabbMin[0], aabbMin[1], aabbMax[2]]
    t = [aabbMin[0], aabbMax[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMin[0], aabbMin[1], aabbMax[2]]
    t = [aabbMax[0], aabbMin[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMax[0], aabbMin[1], aabbMin[2]]
    t = [aabbMax[0], aabbMin[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMax[0], aabbMin[1], aabbMin[2]]
    t = [aabbMax[0], aabbMax[1], aabbMin[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMax[0], aabbMax[1], aabbMin[2]]
    t = [aabbMin[0], aabbMax[1], aabbMin[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMin[0], aabbMax[1], aabbMin[2]]
    t = [aabbMin[0], aabbMax[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMax[0], aabbMax[1], aabbMax[2]]
    t = [aabbMin[0], aabbMax[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1.0, 0.5, 0.5])

    f = [aabbMax[0], aabbMax[1], aabbMax[2]]
    t = [aabbMax[0], aabbMin[1], aabbMax[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])

    f = [aabbMax[0], aabbMax[1], aabbMax[2]]
    t = [aabbMax[0], aabbMax[1], aabbMin[2]]
    bullet_client.addUserDebugLine(f, t, [1, 1, 1])


def main(mesh_dir: str, file_name: str, gui: bool = False) -> None:

    time_str = time.strftime("%Y%m%d-%H%M%S")
    fp_inp = Path(mesh_dir).joinpath(file_name + ".obj")
    fp_out_obj = Path(mesh_dir).joinpath(file_name + "_vhacd.obj")
    fp_out_json = Path(mesh_dir).joinpath(file_name + "_vhacd.json")
    fp_log = Path(mesh_dir).joinpath(time_str + "_" + file_name + "_log.txt")

    mode = p.GUI if gui else p.DIRECT
    bc = BulletClient(connection_mode=mode)
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    for depth in [4]:
        bc.vhacd(str(fp_inp), str(fp_out_obj), str(fp_log), resolution=5000000, depth=depth)

        meshScale = [1, 1, 1]
        collisionShapeId_VHACD = bc.createCollisionShape(shapeType=p.GEOM_MESH,
                                                         fileName=str(fp_out_obj),
                                                         flags=p.URDF_INITIALIZE_SAT_FEATURES,
                                                         meshScale=meshScale)

        body_uid = bc.createMultiBody(baseMass=0,
                                      baseCollisionShapeIndex=collisionShapeId_VHACD,
                                      basePosition=[0, 0, 0],  # 2, depth, 1],
                                      # flags=p.URDF_INITIALIZE_SAT_FEATURES,
                                      useMaximalCoordinates=False)
        collision_shapes = bc.getCollisionShapeData(body_uid, -1)
        data = {'target': str(fp_inp)}
        pos, rpy, dim, aabb, prims = [], [], [], [], []
        for shape_index in range(len(collision_shapes)):
            _, vertices = bc.getMeshData(body_uid, -1, shape_index)

            minX = 1e30
            minY = 1e30
            minZ = 1e30
            maxX = -1e30
            maxY = -1e30
            maxZ = -1e30

            for v in vertices:
                if v[0] < minX:
                    minX = v[0]
                if v[1] < minY:
                    minY = v[1]
                if v[2] < minZ:
                    minZ = v[2]
                if v[0] > maxX:
                    maxX = v[0]
                if v[1] > maxY:
                    maxY = v[1]
                if v[2] > maxZ:
                    maxZ = v[2]

                pos = [(maxX+minX)*0.5, (maxY+minY)*0.5, (maxZ+minZ)*0.5]
                rpy = [0, 0, 0]
                dim = [(maxX-minX)*0.5, (maxY-minY)*0.5, (maxZ-minZ)*0.5]
                aabb = [[pos[0] - dim[0], pos[1] - dim[1], pos[2] - dim[2]],
                        [pos[0] + dim[0], pos[1] + dim[1], pos[2] + dim[2]]]

            if gui:
                drawAABB(bc, aabb)
            prim = {"type": "box", "position": pos, "orientation": rpy, "dimensions": dim}
            prims.append(prim)
        data['primitives'] = prims
        # write a json file
        with fp_out_json.open('w') as json_file:
            json_file.write(jsbeautifier.beautify(json.dumps(data), opts))

    if gui:
        # Reference concave body
        collisionShapeId = bc.createCollisionShape(shapeType=p.GEOM_MESH,
                                                   fileName=str(fp_inp),
                                                   flags=p.URDF_INITIALIZE_SAT_FEATURES + p.GEOM_FORCE_CONCAVE_TRIMESH,
                                                   meshScale=meshScale)
        bc.createMultiBody(baseMass=0,
                           baseCollisionShapeIndex=collisionShapeId,
                           basePosition=[0, 0, 1],
                           flags=p.URDF_INITIALIZE_SAT_FEATURES,
                           useMaximalCoordinates=False)

        # Step simulation and show GUI
        dt = 1./240.
        bc.setGravity(0, 0, -9.81)
        while 1:
            bc.stepSimulation()
            time.sleep(dt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir', help='Directory to the mesh folder', type=str, default="")
    parser.add_argument('--obj_file', help='3D model file as .obj format', type=str, default="bunny.obj")
    parser.add_argument('--gui', action='store_true', help='Option to show result in PyBullet GUI')

    args = parser.parse_args()
    main(mesh_dir=args.dir, file_name=Path(args.obj_file).stem, gui=args.gui)
