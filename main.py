from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block


def build_castle(center, area_size=20, wall_width=2, height=10, offset=5):
    mc.postToChat("<Jokubas012> building the castle")

    # clear area
    distance_from_center = area_size / 2 + wall_width + offset
    offset_vec = Vec3(distance_from_center, 0, distance_from_center)
    start = center + offset_vec
    end = center - offset_vec + Vec3(0, height + offset, 0)
    mc.setBlocks(start, end, block.AIR)

    # build floor
    distance_from_center = area_size / 2 + wall_width
    offset_vec = Vec3(distance_from_center, 0, distance_from_center)
    start = center + offset_vec
    end = center - offset_vec
    mc.setBlocks(start, end, block.STONE_BRICK)

    # build walls
    lt = center + Vec3(-1, 0, 1) * (area_size / 2 + wall_width)
    lb = center + Vec3(-1, 0, -1) * (area_size / 2 + wall_width)
    rt = center + Vec3(1, 0, 1) * (area_size / 2 + wall_width)
    rb = center + Vec3(1, 0, -1) * (area_size / 2 + wall_width)

    # left wall
    start = lb
    end = lt + Vec3(wall_width - 1, height, 0)
    mc.setBlocks(start, end, block.STONE_BRICK)

    # right wall
    start = rb
    end = rt + Vec3(-wall_width + 1, height, 0)
    mc.setBlocks(start, end, block.STONE_BRICK)

    # top wall
    start = lt
    end = rt + Vec3(0, height, -wall_width + 1)
    mc.setBlocks(start, end, block.STONE_BRICK)

    # bottom wall
    start = lb
    end = rb + Vec3(0, height, wall_width - 1)
    mc.setBlocks(start, end, block.STONE_BRICK)

    # gates
    gc = (lt + rt) * 0.5
    start = gc + Vec3(-1, 1, 0)
    end = gc + Vec3(1, 3, -wall_width)
    mc.setBlocks(start, end, block.AIR)


def save_area(fromV, toV, name):
    fx = min(fromV.x, toV.x)
    fy = min(fromV.y, toV.y)
    fz = min(fromV.z, toV.z)
    fromV = Vec3(fx, fy, fz)
    tx = max(fromV.x, toV.x)
    ty = max(fromV.y, toV.y)
    tz = max(fromV.z, toV.z)
    size = Vec3(tx - fx + 1, ty - fy + 1, tz - fz + 1)
    center = Vec3(size.x // 2, size.y // 2, size.z // 2)

    file = open(f"Buildings/{name}.txt", "w")
    for x in range(size.x):
        for y in range(size.y):
            for z in range(size.z):
                id = mc.getBlock(fromV + Vec3(x, y, z))
                if id == block.AIR.id:
                    continue

                file.write(f"{x - center.x},{y - center.y},{z - center.z},{id}\n")

    file.close()


def build_area(center, name):
    file = open(f"Buildings/{name}.txt")
    lines = file.read().split("\n")[:-1]
    file.close()
    for line in lines:
        x, y, z, id = [int(i) for i in line.split(",")]
        vec = center + Vec3(x, y, z)
        mc.setBlock(vec, id)

mc = Minecraft.create()
# build_castle(Vec3(377, 15, 832))
save_area(Vec3(375, 18, 837), Vec3(377, 18, 839), "House")
print(open(f"Buildings/House.txt", "r").read())
build_area(Vec3(378, 20, 839), "House")
build_area(Vec3(378, 21, 839), "House")
build_area(Vec3(378, 22, 839), "House")



