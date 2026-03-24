# 小红书全自动运营系统

> 基于 OpenClaw + Python，实现小红书内容从生成到发布的全自动化

## 这套系统能做什么

- 📅 **定时自动发帖**：每周5条，早段08:00 + 晚段20:00，随机延迟模拟真人
- 🖼️ **自动生成封面图**：高仿真 iOS 备忘录截图风格（v5动态岛/v8经典）
- ✅ **内容双重检核**：自动过滤过时话题、AI味、季节不符
- 💬 **自动回复评论**：随机回复1-2条，口语化，不像机器人
- 📊 **每周数据周报**：自动统计互动率、爆款率，给出优化建议

## 部署步骤

### 第一步：安装依赖

```bash
pip install pillow pilmoji
```

### 第二步：修改脚本路径

打开 `scripts/gen_memo_v5.py`，把所有路径改成你自己的：

```python
# 找到这行，改成你自己的路径
out = 'C:/你的路径/xhs_memo_v5.png'
```

字体路径（Windows默认不用改，Mac/Linux见下方说明）：
```python
# Mac 改为：
f_body = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 33)
# Linux 改为：
f_body = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 33)
```

### 第三步：在 OpenClaw 创建定时任务

共需创建 **4个 Cron Job**，配置见 `docs/cron-jobs.md`

### 第四步：测试运行

```bash
# 测试封面图生成
python scripts/gen_memo_v5.py
# 查看输出的 output_v5.png

# 测试内容检核
python scripts/xhs_content_checker.py
```

## 文件结构

```
xhs-autopilot/
├── README.md              # 本文件
├── scripts/
│   ├── gen_memo_v5.py     # 封面图生成（动态岛版）
│   ├── gen_memo_v8.py     # 封面图生成（经典Home键版）
│   └── xhs_content_checker.py  # 内容检核脚本
└── docs/
    ├── cron-jobs.md       # 4个定时任务配置（复制粘贴即可）
    ├── content-guide.md   # 文案写作规范
    └── anti-ban.md        # 防封号规则
```

## 人设设定

默认人设：**小陈，福州人，26岁，月薪6千，本地生活记录**

修改人设：打开 `docs/cron-jobs.md`，找到 prompt 里的人设描述替换即可

## 注意事项

- 需要小红书账号已在浏览器登录
- 需要 OpenClaw 配置了 browser-use 和 xiaohongshu MCP
- 首次运行建议手动测试每个步骤，确认正常后再开自动
