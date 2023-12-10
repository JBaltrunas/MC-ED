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
    tx = max(fromV.x, toV.x)
    ty = max(fromV.y, toV.y)
    tz = max(fromV.z, toV.z)

    fromV = Vec3(fx, fy, fz)
    size = Vec3(tx - fx + 1, ty - fy + 1, tz - fz + 1)
    center = Vec3(size.x // 2, 0, size.z // 2)

    file = open(f"Buildings/{name}.txt", "w")
    f = -center
    t = size - center
    file.write(f"{f.x},{f.y},{f.z}\n")
    file.write(f"{t.x},{t.y},{t.z}\n")
    for x in range(size.x):
        for y in range(size.y):
            for z in range(size.z):
                b = mc.getBlockWithData(fromV + Vec3(x, y, z))
                if b.id != block.AIR.id:
                    file.write(f"{x - center.x},{y - center.y},{z - center.z},{b.id},{b.data}\n")
    file.close()


def build_area(center, name):
    try:
        file = open(f"Buildings/{name}.txt")
    except:
        mc.postToChat(f"Can't create {name}")
    lines = file.read().split("\n")[:-1]
    file.close()
    f, t = [x.split(",") for x in lines[:2]]
    f = Vec3(int(f[0]), int(f[1]), int(f[2]))
    t = Vec3(int(t[0]), int(t[1]), int(t[2]))
    mc.setBlocks(center - f, center + t, block.AIR)
    for line in lines[2:]:
        x, y, z, id, data = [int(i) for i in line.split(",")]
        vec = center + Vec3(x, y, z)
        mc.setBlock(vec, id, data)


def move_player_to_position(name):
    f = open("Positions/Positions.txt")
    lines = f.read().split("\n")
    f.close()
    for line in lines:
        if line.startswith(name + ','):
            x, y, z = line.split(',')[1:]
            x = int(x)
            y = int(y)
            z = int(z)
            mc.player.setPos(Vec3(x, y, z))
            return
    mc.postToChat(f"Position '{name}' not found")


def save_position(name):
    f = open("Positions/Positions.txt")
    lines = f.read().split("\n")
    f.close()
    for line in lines:
        if line.startswith(name + ','):
            mc.postToChat(f"Position '{name}' already exists")
            f.close()
            return

    f = open("Positions/Positions.txt", "a")
    p = mc.player.getPos()
    f.write(f"{name},{int(p.x)},{int(p.y)},{int(p.z)}\n")
    f.close()


mc = Minecraft.create()

while True:
    posts = mc.events.pollChatPosts()
    for post in posts:
        if post.message == "help":
            mc.postToChat(
                """
                help -> prints all cmds
                bld x,y,z name -> builds building by name on (x, y, z)
                bld name -> builds building by name on player (x, y, z)
                savebld name fx,fy,fz tx,ty,tz -> saves blocks as name from fx,fy,fz to tx,ty,tz
                mp posName -> moves player to selected position
                save posName -> saves position with selected name
                """)
        elif post.message.startswith("bld"):
            l = post.message.split(" ")
            if len(l) == 2 or len(l) == 3:
                if len(l) == 2:
                    pos = mc.player.getPos()
                    name = l[1]
                else:
                    try:
                        pos = [int(x) for x in l[1].split(",")]
                        pos = Vec3(pos[0], pos[1], pos[2])
                        name = l[2]
                    except:
                        mc.postToChat("Invalid coords")

                build_area(pos, name)
            else:
                mc.postToChat("To many args")
        elif post.message.startswith('mp'):
            words = post.message.split(" ")
            if len(words) == 2:
                pname = words[1]
                move_player_to_position(pname)
            else:
                mc.postToChat("To many args")
        elif post.message.startswith("save"):
            words = post.message.split(" ")
            if len(words) == 2:
                pname = words[1]
                save_position(pname)
            else:
                mc.postToChat("To many args")
        elif post.message.startswith("savebld"):
            l = post.message.split(" ")
            if len(l) == 4:
                name = l[1]
                try:
                    pos = [int(x) for x in l[2].split(",")]
                    f = Vec3(pos[0], pos[1], pos[2])
                    pos = [int(x) for x in l[3].split(",")]
                    t = Vec3(pos[0], pos[1], pos[2])
                    save_area(f, t, name)
                except:
                    mc.postToChat("Invalid coords")
            else:
                mc.postToChat("Invalid count of args")
        else:
            mc.postToChat("Unknown cmd")

