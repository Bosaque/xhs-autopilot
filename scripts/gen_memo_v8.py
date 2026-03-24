# -*- coding: utf-8 -*-
"""
高仿真 iOS 备忘录截图 v8
基于v7迭代细节：导航栏胶囊/返回按钮阴影/行间距/工具栏
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pilmoji import Pilmoji

W, H = 1080, 1440
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

black     = (0, 0, 0)
dark      = (0, 0, 0)
gray_date = (142, 142, 147)
gray_sec  = (60, 60, 67)
gray_mid  = (142, 142, 147)
gray_lt   = (199, 199, 204)
divider   = (230, 230, 230)     # 更浅的分割线
ios_green = (52, 199, 89)
toolbar_bg= (242, 242, 247)

f_time    = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   26)
f_date    = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   22)   # 日期行更小
f_title   = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 36)
f_body    = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   33)
f_body_sm = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   29)
f_small   = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   22)
f_sym     = ImageFont.truetype('C:/Windows/Fonts/seguisym.ttf', 30)
f_arrow   = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 36)
f_btn     = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 26)


def draw_signal_bars(x, y, color, filled=3):
    bar_w, gap = 7, 5
    heights = [10, 16, 22, 29]
    base = y + 30
    for i, h in enumerate(heights):
        bx = x + i*(bar_w+gap)
        if i < filled:
            d.rounded_rectangle([(bx,base-h),(bx+bar_w,base)], radius=2, fill=color)
        else:
            d.rounded_rectangle([(bx,base-h),(bx+bar_w,base)], radius=2, outline=color, width=2)

def draw_wifi(x, y, color):
    cx, cy = x+17, y+30
    d.ellipse([(cx-4,cy-4),(cx+4,cy+4)], fill=color)
    for r, lw in [(9,4),(16,4),(23,4)]:
        d.arc([cx-r,cy-r,cx+r,cy+r], start=215, end=325, fill=color, width=lw)

def draw_battery(x, y, pct=60):
    bw, bh, rx = 50, 24, 5
    d.rounded_rectangle([(x,y),(x+bw,y+bh)], radius=rx, outline=black, width=2)
    hx, hy = x+bw+2, y+(bh-12)//2
    d.rounded_rectangle([(hx,hy),(hx+5,hy+12)], radius=2, fill=black)
    iw = int((bw-6)*pct/100)
    if iw > 0:
        d.rounded_rectangle([(x+3,y+3),(x+3+iw,y+bh-3)], radius=3, fill=black)

def draw_circle_btn(cx, cy, r, sym, font):
    """立体圆形按钮：白底+浅灰阴影效果"""
    # 阴影层（偏移1-2px，浅灰）
    d.ellipse([(cx-r+2, cy-r+2),(cx+r+2, cy+r+2)], fill=(210,210,215))
    # 主体白圆
    d.ellipse([(cx-r, cy-r),(cx+r, cy+r)], fill=(242,242,247))
    # 文字居中
    tw = d.textbbox((0,0), sym, font=font)
    tx = cx - (tw[2]-tw[0])//2
    ty = cy - (tw[3]-tw[1])//2 - 2
    d.text((tx, ty), sym, font=font, fill=black)


# ══════════════════════════════════════════════
# 1. 状态栏
# ══════════════════════════════════════════════
status_h = 54
d.rectangle([(0,0),(W,status_h)], fill=(255,255,255))
d.text((44, 14), '22:17', font=f_time, fill=black)

batt_x = W - 114
draw_battery(batt_x, 16, pct=60)
draw_wifi(batt_x-58, 12, color=black)
draw_signal_bars(batt_x-120, 12, color=black, filled=3)
y = status_h

# ══════════════════════════════════════════════
# 2. 导航栏
# ══════════════════════════════════════════════
nav_h = 92
d.rectangle([(0,y),(W,y+nav_h)], fill=(255,255,255))
btn_cy = y + nav_h//2

# 左：立体圆形返回按钮
draw_circle_btn(60, btn_cy, 28, '<', f_arrow)

# 右：分享+三点 合进一个圆角胶囊
cap_w, cap_h = 160, 56
cap_x = W - cap_w - 30
cap_y = btn_cy - cap_h//2
# 胶囊阴影
d.rounded_rectangle(
    [(cap_x+2, cap_y+2),(cap_x+cap_w+2, cap_y+cap_h+2)],
    radius=28, fill=(210,210,215)
)
# 胶囊主体
d.rounded_rectangle(
    [(cap_x, cap_y),(cap_x+cap_w, cap_y+cap_h)],
    radius=28, fill=(242,242,247)
)
# 分割线
mid_x = cap_x + cap_w//2
d.line([(mid_x, cap_y+12),(mid_x, cap_y+cap_h-12)], fill=(200,200,205), width=1)
# 左：分享图标（↑ + 小方框）
share_cx = cap_x + cap_w//4
d.text((share_cx-10, btn_cy-18), '↑', font=f_btn, fill=black)
d.rectangle([(share_cx-10, btn_cy+2),(share_cx+10, btn_cy+14)], outline=black, width=2)
# 右：三点
dot_cx = cap_x + cap_w*3//4
tw = d.textbbox((0,0), '···', font=f_btn)
d.text((dot_cx-(tw[2]-tw[0])//2, btn_cy-12), '···', font=f_btn, fill=black)

# 导航栏分割线（极细极浅）
d.line([(0,y+nav_h-1),(W,y+nav_h-1)], fill=(240,240,240), width=1)
y += nav_h

# ══════════════════════════════════════════════
# 3. 日期行（更宽松间距）
# ══════════════════════════════════════════════
y += 30   # 上间距更大
date_text = '2026年3月25日  08:12'
tw = d.textbbox((0,0), date_text, font=f_date)
d.text(((W-(tw[2]-tw[0]))//2, y), date_text, font=f_date, fill=gray_date)
y += 56   # 下间距更大

# ══════════════════════════════════════════════
# 4. 正文（行间距放大，更透气）
# ══════════════════════════════════════════════
px     = 40
LINE_H = 56   # 放大，更透气
PARA_H = 32

lines = [
    ('之前觉得6千在福州存不了钱', f_body, dark),
    ('房租1200 吃饭800 交通200', f_body, dark),
    ('剩下的不知道哪去了...', f_body, dark),
    (None, None, None),
    ('认真记了3个月账才发现', f_body, dark),
    ('钱都漏在这几个地方 👇', f_body, dark),
    (None, None, None),
    ('外卖：每月将近600', f_body_sm, gray_sec),
    ('奶茶咖啡：400多', f_body_sm, gray_sec),
    ('周末随便逛逛：300', f_body_sm, gray_sec),
    (None, None, None),
    ('现在的做法：', f_body, dark),
    ('发工资当天先存2000', f_body, dark),
    ('剩下的才是生活费', f_body, dark),
    ('强制储蓄，不然真存不住', f_body, dark),
    (None, None, None),
    ('自己买菜一周省200左右', f_body_sm, gray_sec),
    ('三个月攒了5000多', f_body_sm, gray_sec),
    ('对我来说已经很满足了 😊', f_body_sm, gray_sec),
    (None, None, None),
    ('不是要抠死自己', f_body, dark),
    ('找到最大漏钱点堵住就行', f_body, dark),
    (None, None, None),
    ('你们月薪多少，能存多少？', f_body_sm, gray_mid),
    (None, None, None),
    ('补充一下我的固定支出', f_body_sm, gray_sec),
    ('房租 1200 / 手机话费 99', f_body_sm, gray_sec),
    ('健身房年卡摊下来 80/月', f_body_sm, gray_sec),
    ('这些没办法省的就不省', f_body_sm, gray_sec),
    (None, None, None),
    ('能省的是弹性支出', f_body_sm, gray_sec),
    ('外卖→自己做，省一半', f_body_sm, gray_sec),
    ('奶茶→自己冲咖啡，省80%', f_body_sm, gray_sec),
    (None, None, None),
    ('慢慢来，别给自己太大压力', f_body_sm, gray_mid),
    ('存钱是习惯，不是苦行 😮', f_body_sm, gray_mid),
]

with Pilmoji(img) as p:
    for text, font, color in lines:
        if text is None:
            y += PARA_H
            continue
        p.text((px, y), text, font=font, fill=color)
        y += LINE_H

# ══════════════════════════════════════════════
# 5. 底部工具栏（对照参考图）
# ══════════════════════════════════════════════
tool_y = H - 100
d.rectangle([(0,tool_y),(W,H)], fill=(255,255,255))
# 极细分割线
d.line([(0,tool_y),(W,tool_y)], fill=(240,240,240), width=1)

# 左侧胶囊（3图标）- 阴影+主体
gx, gy, gw, gh = 36, tool_y+16, 270, 66
d.rounded_rectangle([(gx+2,gy+2),(gx+gw+2,gy+gh+2)], radius=16, fill=(210,210,215))
d.rounded_rectangle([(gx,gy),(gx+gw,gy+gh)], radius=16, fill=toolbar_bg)

# 分割线（图标之间）
step = gw//3
for i in [1,2]:
    lx = gx + i*step
    d.line([(lx, gy+14),(lx, gy+gh-14)], fill=(200,200,205), width=1)

# 3个图标：带圈列表 / 回形针 / Aa
icons_pos = [gx+step//2, gx+step+step//2, gx+2*step+step//2]
icon_syms = ['☰', '⌀', 'Aa']
for ix, sym in zip(icons_pos, icon_syms):
    try:
        tw2 = d.textbbox((0,0), sym, font=f_sym)
        d.text((ix-(tw2[2]-tw2[0])//2, gy+16), sym, font=f_sym, fill=black)
    except: pass

# 右侧：方形白底铅笔按钮（立体）
pen_cx, pen_cy = W-58, tool_y+50
# 阴影
d.rounded_rectangle([(pen_cx-28,pen_cy-28+2),(pen_cx+28,pen_cy+28+2)], radius=10, fill=(210,210,215))
# 主体
d.rounded_rectangle([(pen_cx-28,pen_cy-28),(pen_cx+28,pen_cy+28)], radius=10, fill=(255,255,255))
# 铅笔图标
try:
    tw3 = d.textbbox((0,0),'✏',font=f_sym)
    d.text((pen_cx-(tw3[2]-tw3[0])//2, pen_cy-16), '✏', font=f_sym, fill=black)
except: pass

# Home指示条（更细更短）
home_w = 220
hx = (W-home_w)//2
d.rounded_rectangle([(hx,H-13),(hx+home_w,H-7)], radius=3, fill=(190,190,192))

out = 'C:/Users/admin/.easyclaw/workspace/xhs_memo_v8.png'
img.save(out)
print(f'[OK] {out}')
