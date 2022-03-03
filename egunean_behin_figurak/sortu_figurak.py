from PIL import Image, ImageDraw
import random

koloreak = ["red", "green", "blue"]
canvas = (600, 400)
scale = 1
thumb = canvas[0]/scale, canvas[1]/scale


n_x=range(1,13)
n_y=range(1,9)
pausoa_x=thumb[0]/(len(n_x)+1)
pausoa_y=thumb[1]/(len(n_y)+1)
r=16

def marraztu_borobila(draw, x,y,r):
    kolorea = random.randint(0,2)
    draw.ellipse((x-r, y-r, x+r, y+r), fill=koloreak[kolorea])
    return kolorea

def marraztu_karratua(draw, x,y,r):
    kolorea = random.randint(0,2)
    draw.rectangle([x-r, y-r, x+r, y+r], fill=koloreak[kolorea])
    return kolorea

def marraztu_triangelua(draw, x,y,r):
    kolorea = random.randint(0,2)
    draw.polygon([(x-r,y+r), (x+r, y+r), (x,y-r)], fill=koloreak[kolorea])
    return kolorea


marraztu_figurak = [marraztu_triangelua, marraztu_karratua, marraztu_borobila]

def marraztu_galdera(i):
    im = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    # 0hirukia, 1laukia, 2borobila / 0red, 1green, 2blue
    iz={'00':0, '01':0, '02':0, '10':0, '11':0, '12':0, '20':0, '21':0, '22':0}

    for y1 in n_y:
        for x1 in n_x:
            x=x1*pausoa_x
            y=y1*pausoa_y
            figura = random.randint(0,2)
            color = marraztu_figurak[figura](draw, x,y,r)
            iz[str(figura)+str(color)]+=1

    im.thumbnail(thumb)
    im.save('./figurak/fig_%d_%d_%d_%d_%d_%d_%d_%d_%d.png'%(iz['00'], iz['01'], iz['02'], iz['10'], iz['11'], iz['12'], iz['20'], iz['21'], iz['22']))

if __name__ == '__main__':
    zenbat_galdera=range(0,20)
    for galdera in zenbat_galdera:
        marraztu_galdera(galdera)
