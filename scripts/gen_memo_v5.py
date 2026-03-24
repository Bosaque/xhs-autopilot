# -*- coding: utf-8 -*-
"""
高仿真 iOS 备忘录截图 v5
PIL精准还原，无AI感，像素级控制
关键修复：标题字号接近正文/去分割线/动态岛摄像头/工具栏图标
"""
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

W, H = 1080, 1440
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# ── 颜色（严格对照iOS真实值）──────────────────
bg        = (255, 255, 255)
black     = (0, 0, 0)           # 纯黑，iOS文字
dark      = (0, 0, 0)
gray_sec  = (60, 60, 67)        # iOS secondary label
gray_mid  = (142, 142, 147)     # iOS systemGray
gray_lt   = (199, 199, 204)     # iOS systemGray3
divider   = (209, 209, 214)     # iOS separator
ios_blue  = (0, 122, 255)
ios_green = (52, 199, 89)
cursor_c  = (0, 122, 255)
dyn_black = (0, 0, 0)
toolbar_bg= (249, 249, 249)

# ── 字体 ──────────────────────────────────────
# 正文用细体，标题只比正文大一点点
f_time    = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   26)
f_nav     = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   30)
f_nav_b   = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 30)
f_title   = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 36)   # 只比正文大一点
f_body    = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   33)   # 正文
f_body_sm = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   29)   # 次要文字
f_small   = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',   23)
f_chevron = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 42)

# ══════════════════════════════════════════════
# 状态栏图标（PIL精绘）
# ══════════════════════════════════════════════
def draw_signal(d, x, y, color):
    bar_w, gap = 6, 4
    heights = [10, 16, 22, 29]
    base = y + 30
    for i, h in enumerate(heights):
        bx = x + i * (bar_w + gap)
        d.rounded_rectangle([(bx, base-h),(bx+bar_w, base)], radius=2, fill=color)

def draw_wifi(d, x, y, color):
    cx, cy = x+17, y+30
    d.ellipse([(cx-4,cy-4),(cx+4,cy+4)], fill=color)
    for r, lw in [(9,4),(16,4),(23,4)]:
        d.arc([cx-r,cy-r,cx+r,cy+r], start=215, end=325, fill=color, width=lw)

def draw_battery(d, x, y, pct=74):
    bw, bh, rx = 50, 24, 5
    d.rounded_rectangle([(x,y),(x+bw,y+bh)], radius=rx, outline=black, width=2)
    hx, hy = x+bw+2, y+(bh-12)//2
    d.rounded_rectangle([(hx,hy),(hx+5,hy+12)], radius=2, fill=black)
    iw = int((bw-6)*pct/100)
    if iw > 0:
        d.rounded_rectangle([(x+3,y+3),(x+3+iw,y+bh-3)], radius=3, fill=ios_green)

# ══════════════════════════════════════════════
# 1. 动态岛（含摄像头圆点）
# ══════════════════════════════════════════════
status_h = 58
d.rectangle([(0,0),(W,status_h)], fill=bg)

di_w, di_h = 252, 36
di_x = (W - di_w) // 2
di_y = 12
d.rounded_rectangle([(di_x,di_y),(di_x+di_w,di_y+di_h)], radius=18, fill=dyn_black)
# 摄像头圆点（右侧）
cam_cx = di_x + di_w - 22
cam_cy = di_y + di_h // 2
d.ellipse([(cam_cx-8,cam_cy-8),(cam_cx+8,cam_cy+8)], fill=(20,20,20))
d.ellipse([(cam_cx-4,cam_cy-4),(cam_cx+4,cam_cy+4)], fill=(35,35,35))
# 传感器小点（摄像头左侧）
sen_cx = cam_cx - 24
d.ellipse([(sen_cx-4,cam_cy-4),(sen_cx+4,cam_cy+4)], fill=(25,25,25))

# ── 状态栏内容 ─────────────────────────────────
d.text((44, 17), '22:17', font=f_time, fill=black)

batt_x = W - 116
draw_battery(d, batt_x, 18, pct=74)
wifi_x = batt_x - 56
draw_wifi(d, wifi_x, 14, color=black)
sig_x = wifi_x - 56
draw_signal(d, sig_x, 14, color=black)

y = status_h

# ══════════════════════════════════════════════
# 2. 导航栏
# ══════════════════════════════════════════════
nav_h = 78
d.rectangle([(0,y),(W,y+nav_h)], fill=bg)
d.text((32, y+18), '‹', font=f_chevron, fill=ios_blue)
d.text((64, y+23), '备忘录', font=f_nav, fill=ios_blue)
d.text((W-84, y+23), '完成', font=f_nav, fill=ios_blue)  # Regular，不加粗
d.line([(0,y+nav_h-1),(W,y+nav_h-1)], fill=divider, width=1)
y += nav_h

# ══════════════════════════════════════════════
# 3. 内容区
# ══════════════════════════════════════════════
px     = 56
LINE_H = 52
PARA_H = 20
y += 36

# 标题：字号接近正文，只是加粗，不加分割线
d.text((px, y), '月薪6千在福州存钱记录', font=f_title, fill=dark)
y += 62   # 标题后间距略大，模拟iOS自动段落间距

# 正文（无分割线，直接开始）
lines = [
    ('之前觉得6千在福州存不了钱 😮', f_body, dark),
    ('房租1200 吃饭800 交通200', f_body, dark),
    ('剩下的不知道哪去了... 😭', f_body, dark),
    (None, None, None),
    ('认真记了3个月账才发现 📒', f_body, dark),
    ('钱都漏在这几个地方 👇', f_body, dark),
    (None, None, None),
    ('🥡 外卖：每月将近600', f_body_sm, gray_sec),
    ('🧋 奶茶咖啡：400多', f_body_sm, gray_sec),
    ('🛍️ 周末随便逛逛：300', f_body_sm, gray_sec),
    (None, None, None),
    ('💡 现在的做法：', f_body, dark),
    ('发工资当天先存2000 💰', f_body, dark),
    ('剩下的才是生活费', f_body, dark),
    ('强制储蓄，不然真存不住', f_body, dark),
    (None, None, None),
    ('自己买菜一周省200左右 🥬', f_body_sm, gray_sec),
    ('三个月攒了5000多 🎉', f_body_sm, gray_sec),
    ('对我来说已经很满足了', f_body_sm, gray_sec),
    (None, None, None),
    ('固定支出没办法省 📌', f_body_sm, gray_sec),
    ('房租1200 / 话费99 / 健身80', f_body_sm, gray_sec),
    ('这些认了，省弹性支出就行', f_body_sm, gray_sec),
    (None, None, None),
    ('不是要抠死自己 🙅', f_body, dark),
    ('找到最大漏钱点堵住就行', f_body, dark),
    (None, None, None),
    ('你们月薪多少，能存多少？', f_body_sm, gray_mid),
    ('评论区说说 😊', f_body_sm, gray_mid),
]

with Pilmoji(img) as p:
    for text, font, color in lines:
        if text is None:
            y += PARA_H
            continue
        p.text((px, y), text, font=font, fill=color)
        y += LINE_H

# 最后不完整行 + 光标
last = '租金多少'
d.text((px, y), last, font=f_body_sm, fill=gray_lt)
tw = d.textbbox((0,0), last, font=f_body_sm)
cx = px + (tw[2]-tw[0]) + 3
d.rectangle([(cx, y+3),(cx+2, y+30)], fill=cursor_c)

# ══════════════════════════════════════════════
# 4. 底部工具栏（Unicode图标，比文字更像SF Symbols）
# ══════════════════════════════════════════════
tool_y = H - 108
d.rectangle([(0,tool_y),(W,H)], fill=toolbar_bg)
d.line([(0,tool_y),(W,tool_y)], fill=divider, width=1)

# 用更像工具图标的Unicode字符
tool_icons = [
    ('⊞', '表格'),
    ('☑', '勾选'),
    ('⬜', '图片'),
    ('⊙', '相机'),
    ('✎', '画笔'),
    ('⊡', '扫描'),
]
step = (W - 80) // len(tool_icons)
ix = 40
f_icon_sym = ImageFont.truetype('C:/Windows/Fonts/seguisym.ttf', 30)
for sym, label in tool_icons:
    try:
        tw2 = d.textbbox((0,0), sym, font=f_icon_sym)
        d.text((ix-(tw2[2]-tw2[0])//2, tool_y+18), sym, font=f_icon_sym, fill=gray_mid)
    except:
        tw2 = d.textbbox((0,0), label, font=f_small)
        d.text((ix-(tw2[2]-tw2[0])//2, tool_y+20), label, font=f_small, fill=gray_mid)
    ix += step

# Home 指示条
home_w = 260
hx = (W - home_w) // 2
d.rounded_rectangle([(hx, H-16),(hx+home_w, H-8)], radius=4, fill=(180,180,182))

# ══════════════════════════════════════════════
out = 'C:/Users/admin/.easyclaw/workspace/xhs_memo_v5.png'
img.save(out)
print(f'[OK] {out}')


