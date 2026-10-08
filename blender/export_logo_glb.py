"""
Exporta a logo 3D do .blend para GLB, com material na cor da marca.

Uso (Windows, PowerShell):
  & "C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe" -b `
    "C:\\Users\\Lucas Micael\\Documents\\Logo M - Desintegration.blend" `
    --python export_logo_glb.py -- `
    --out "C:\\Users\\Lucas Micael\\Documents\\logo-m.glb"

Argumentos opcionais (depois do "--"):
  --out PATH       caminho do .glb (padrao: ao lado do .blend)
  --color HEX      cor da marca (padrao: #6DFDC8)
  --frame N        frame usado na exportacao (padrao: frame inicial da cena,
                   antes da desintegracao)
  --metallic F     0..1 (padrao: 0.0)
  --roughness F    0..1 (padrao: 0.35)
  --draco          comprime a malha com Draco (menor, ideal para web)
  --objects A,B    exporta so esses objetos (padrao: todas as malhas,
                   curvas e textos visiveis no render)
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out")
    p.add_argument("--color", default="#6DFDC8")
    p.add_argument("--frame", type=int)
    p.add_argument("--metallic", type=float, default=0.0)
    p.add_argument("--roughness", type=float, default=0.35)
    p.add_argument("--draco", action="store_true")
    p.add_argument("--objects")
    return p.parse_args(argv)


def srgb_hex_to_linear(hex_color):
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return (*lin, 1.0)


def brand_material(color, metallic, roughness):
    mat = bpy.data.materials.new("Brand")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def main():
    args = parse_args()
    scene = bpy.context.scene
    scene.frame_set(args.frame if args.frame is not None else scene.frame_start)

    if args.objects:
        names = [n.strip() for n in args.objects.split(",")]
        sources = [bpy.data.objects[n] for n in names]
    else:
        sources = [
            o for o in scene.objects
            if o.type in {"MESH", "CURVE", "FONT", "SURFACE", "META"}
            and not o.hide_render
        ]
    if not sources:
        sys.exit("Nenhum objeto exportavel encontrado.")

    # Congela o estado avaliado (modificadores, geometry nodes, animacao)
    # em malhas novas, numa colecao separada.
    out_coll = bpy.data.collections.new("GLB_Export")
    scene.collection.children.link(out_coll)
    mat = brand_material(srgb_hex_to_linear(args.color), args.metallic, args.roughness)
    depsgraph = bpy.context.evaluated_depsgraph_get()

    for src in sources:
        evaluated = src.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph)
        if not mesh.polygons:
            continue
        mesh.materials.clear()
        mesh.materials.append(mat)
        obj = bpy.data.objects.new(src.name, mesh)
        obj.matrix_world = src.matrix_world.copy()
        out_coll.objects.link(obj)
        print(f"  + {src.name}: {len(mesh.polygons)} faces")

    if not out_coll.objects:
        sys.exit("Os objetos nao tem faces nesse frame. Tente outro --frame.")

    bpy.ops.object.select_all(action="DESELECT")
    for o in out_coll.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = out_coll.objects[0]

    out = args.out or os.path.splitext(bpy.data.filepath)[0] + ".glb"
    bpy.ops.export_scene.gltf(
        filepath=out,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_animations=False,
        export_cameras=False,
        export_lights=False,
        export_yup=True,
        export_draco_mesh_compression_enable=args.draco,
    )
    print(f"GLB exportado: {out}")


main()
