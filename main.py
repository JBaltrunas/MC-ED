from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block


def build_castle(center):
    area_size = 100
    wall_width = 5
    height = 20
    offset = 20
    mc.postToChat("<Jokubas012> building the castle")

    # clear area
    distance_from_center = area_size / 2 + wall_width + offset
    offset_vec: Vec3 = Vec3(distance_from_center, 0, distance_from_center)
    start = center + offset_vec
    end = center - offset_vec + Vec3(0, height * 5, 0)
    mc.setBlocks(start, end, block.AIR)



    # build floor
    distance_from_center = area_size / 2 + wall_width
    offset_vec = Vec3(distance_from_center, 0, distance_from_center)
    start = center + offset_vec
    end = center - offset_vec
    mc.setBlocks(start, end, block.STONE_BRICK)





mc = Minecraft.create()
build_castle(Vec3(520, 67, 167))


