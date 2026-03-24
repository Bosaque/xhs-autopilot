# -*- coding: utf-8 -*-
"""
小红书内容检核系统
自动审核内容是否过时、是否符合当下
"""
import datetime
import re

class ContentChecker:
    """内容检核器"""
    
    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.current_month = self.current_date.month
        self.season = self._get_season()
        
    def _get_season(self):
        """获取当前季节"""
        month = self.current_month
        if month in [3, 4, 5]:
            return "春季"
        elif month in [6, 7, 8]:
            return "夏季"
        elif month in [9, 10, 11]:
            return "秋季"
        else:
            return "冬季"
    
    def check_outdated_topics(self, content):
        """检查过时话题"""
        outdated_keywords = {
            "过年": {"valid_months": [1, 2], "alternative": "换季/春天"},
            "春节": {"valid_months": [1, 2], "alternative": "换季/春天"},
            "年夜饭": {"valid_months": [1, 2], "alternative": "外卖/食堂"},
            "年终奖": {"valid_months": [1, 2], "alternative": "工资/奖金"},
            "拜年": {"valid_months": [1, 2], "alternative": "同事聚会"},
            "红包": {"valid_months": [1, 2], "alternative": "省钱/存款"},
            "国庆": {"valid_months": [9, 10], "alternative": "周末/假期"},
            "中秋": {"valid_months": [9], "alternative": "周末/聚餐"},
            "双11": {"valid_months": [10, 11], "alternative": "日常消费"},
            "双12": {"valid_months": [11, 12], "alternative": "日常消费"},
            "618": {"valid_months": [5, 6], "alternative": "日常购物"},
        }
        
        issues = []
        for keyword, info in outdated_keywords.items():
            if keyword in content:
                if self.current_month not in info["valid_months"]:
                    issues.append({
                        "keyword": keyword,
                        "issue": f"'{keyword}'已过时（当前{self.current_month}月，该话题仅在{info['valid_months']}月有效）",
                        "suggestion": f"建议替换为：{info['alternative']}"
                    })
        
        return issues
    
    def check_season_relevance(self, content):
        """检查季节相关性"""
        season_keywords = {
            "春季": ["春天", "换季", "感冒", "过敏", "回南天", "潮湿", "花开", "春游"],
            "夏季": ["夏天", "高温", "空调", "电费", "西瓜", "防晒", "暴雨", "台风"],
            "秋季": ["秋天", "降温", "秋招", "换季", "干燥", "贴秋膘", "开学"],
            "冬季": ["冬天", "寒冷", "取暖", "电费", "春运", "年末", "年终"],
        }
        
        current_season_keywords = season_keywords.get(self.season, [])
        
        # 检查是否有其他季节的关键词
        other_season_issues = []
        for season, keywords in season_keywords.items():
            if season != self.season:
                for keyword in keywords:
                    if keyword in content:
                        other_season_issues.append({
                            "keyword": keyword,
                            "issue": f"内容包含'{season}'关键词'{keyword}'，但当前是{self.season}（{self.current_month}月）",
                            "suggestion": f"建议替换为{self.season}相关话题：{', '.join(current_season_keywords[:3])}"
                        })
        
        return other_season_issues
    
    def check_ai_tone(self, content):
        """检查AI味"""
        ai_keywords = [
            "首先", "其次", "然后", "接着", "最后",
            "综上所述", "总而言之", "由此可见",
            "不难发现", "值得注意的是", "我们可以看到",
            "究其原因", "从某种程度上说", "从某种意义上讲",
            "值得一提的是", "不得不指出", "毫无疑问",
        ]
        
        issues = []
        for keyword in ai_keywords:
            if keyword in content:
                issues.append({
                    "keyword": keyword,
                    "issue": f"检测到AI常用词'{keyword}'",
                    "suggestion": "替换为口语化表达：哎/就是/真的/emo/绝了"
                })
        
        return issues
    
    def check_engagement_hooks(self, content):
        """检查互动钩子"""
        hooks = [
            "评论区", "打", "你是哪种", "你是", "告诉我",
            "说出来", "让我看看", "比", "吐槽", "一起"
        ]
        
        has_hook = any(hook in content for hook in hooks)
        
        if not has_hook:
            return [{
                "issue": "内容缺少互动钩子",
                "suggestion": "添加互动引导：评论区打ABCD/你是哪种/说出来让我看看"
            }]
        
        return []
    
    def check_numbers(self, content):
        """检查是否有具体数字"""
        numbers = re.findall(r'\d+', content)
        
        if len(numbers) < 3:
            return [{
                "issue": "内容数字太少",
                "suggestion": "添加具体数字：价格、时间、数量等，增加真实感"
            }]
        
        return []
    
    def check_first_person(self, content):
        """检查第一人称"""
        first_person = ["我", "我的"]
        has_first = any(fp in content for fp in first_person)
        
        if not has_first:
            return [{
                "issue": "缺少第一人称",
                "suggestion": "用'我'来讲述，增加代入感和真实性"
            }]
        
        return []
    
    def full_check(self, title, content):
        """完整检核"""
        all_issues = []
        
        # 各项检查
        all_issues.extend(self.check_outdated_topics(content))
        all_issues.extend(self.check_season_relevance(content))
        all_issues.extend(self.check_ai_tone(content))
        all_issues.extend(self.check_engagement_hooks(content))
        all_issues.extend(self.check_numbers(content))
        all_issues.extend(self.check_first_person(content))
        
        # 生成报告
        report = {
            "check_time": self.current_date.strftime("%Y-%m-%d %H:%M"),
            "current_season": self.season,
            "title": title,
            "issues_count": len(all_issues),
            "issues": all_issues,
            "status": "✅ 通过" if len(all_issues) == 0 else "❌ 需修改"
        }
        
        return report
    
    def print_report(self, report):
        """打印检核报告"""
        print("=" * 60)
        print(f"📋 小红书内容检核报告")
        print("=" * 60)
        print(f"检核时间：{report['check_time']}")
        print(f"当前季节：{report['current_season']}")
        print(f"标题：{report['title']}")
        print(f"状态：{report['status']}")
        print(f"问题数：{report['issues_count']}")
        
        if report['issues']:
            print("\n⚠️ 发现问题：")
            for i, issue in enumerate(report['issues'], 1):
                print(f"\n{i}. 问题：{issue.get('issue', 'N/A')}")
                if 'keyword' in issue:
                    print(f"   关键词：{issue['keyword']}")
                print(f"   建议：{issue.get('suggestion', 'N/A')}")
        else:
            print("\n✅ 内容检核通过！")
        
        print("=" * 60)


# 使用示例
if __name__ == "__main__":
    checker = ContentChecker()
    
    # 测试内容
    test_title = "福州3月换季，我又双叒叕感冒了"
    test_content = """福州这天气，我真的服了

昨天30度，今天15度
早上穿羽绒服，中午穿短袖

换季一周，感冒3天
请假扣了500块工资

你是哪种？评论区告诉我"""
    
    report = checker.full_check(test_title, test_content)
    checker.print_report(report)
