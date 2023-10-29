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


mc = Minecraft.create()
build_castle(Vec3(377, 15, 832))


