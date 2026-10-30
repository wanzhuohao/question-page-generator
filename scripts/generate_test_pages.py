#!/usr/bin/env python3
"""
测试脚本：用 uniapp 项目中的实际题型数据结构生成 HTML 页面，验证模板渲染。
"""

import json
import re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "template.html"
OUTPUT_DIR = Path(__file__).parent / "test-output"

# 测试用例：覆盖 uniapp 项目中所有题型
TEST_CASES = [
    # ===== 纯计算题（打印模式用 3 列网格）=====
    {
        "name": "add",
        "title": "加法练习",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "add", "expr": "12 + 7", "answer": "19", "userAnswer": ""},
            {"id": 2, "type": "add", "expr": "23 + 8", "answer": "31", "userAnswer": ""},
            {"id": 3, "type": "add", "expr": "15 + 6", "answer": "21", "userAnswer": ""},
            {"id": 4, "type": "add", "expr": "9 + 14", "answer": "23", "userAnswer": ""},
            {"id": 5, "type": "add", "expr": "7 + 8", "answer": "15", "userAnswer": ""},
            {"id": 6, "type": "add", "expr": "16 + 5", "answer": "21", "userAnswer": ""},
            {"id": 7, "type": "add", "expr": "4 + 13", "answer": "17", "userAnswer": ""},
            {"id": 8, "type": "add", "expr": "11 + 9", "answer": "20", "userAnswer": ""},
            {"id": 9, "type": "add", "expr": "18 + 3", "answer": "21", "userAnswer": ""},
            {"id": 10, "type": "add", "expr": "6 + 7", "answer": "13", "userAnswer": ""},
        ]
    },
    {
        "name": "sub",
        "title": "减法练习",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "sub", "expr": "15 - 8", "answer": "7", "userAnswer": ""},
            {"id": 2, "type": "sub", "expr": "23 - 9", "answer": "14", "userAnswer": ""},
            {"id": 3, "type": "sub", "expr": "17 - 5", "answer": "12", "userAnswer": ""},
            {"id": 4, "type": "sub", "expr": "14 - 6", "answer": "8", "userAnswer": ""},
            {"id": 5, "type": "sub", "expr": "19 - 7", "answer": "12", "userAnswer": ""},
            {"id": 6, "type": "sub", "expr": "21 - 4", "answer": "17", "userAnswer": ""},
            {"id": 7, "type": "sub", "expr": "13 - 5", "answer": "8", "userAnswer": ""},
            {"id": 8, "type": "sub", "expr": "18 - 9", "answer": "9", "userAnswer": ""},
        ]
    },
    {
        "name": "mixed-calc",
        "title": "口算混合练习",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "add", "expr": "12 + 7", "answer": "19", "userAnswer": ""},
            {"id": 2, "type": "sub", "expr": "15 - 8", "answer": "7", "userAnswer": ""},
            {"id": 3, "type": "add", "expr": "9 + 6", "answer": "15", "userAnswer": ""},
            {"id": 4, "type": "sub", "expr": "14 - 5", "answer": "9", "userAnswer": ""},
            {"id": 5, "type": "add", "expr": "8 + 7", "answer": "15", "userAnswer": ""},
            {"id": 6, "type": "sub", "expr": "13 - 6", "answer": "7", "userAnswer": ""},
            {"id": 7, "type": "add", "expr": "11 + 5", "answer": "16", "userAnswer": ""},
            {"id": 8, "type": "sub", "expr": "17 - 8", "answer": "9", "userAnswer": ""},
            {"id": 9, "type": "add", "expr": "4 + 9", "answer": "13", "userAnswer": ""},
            {"id": 10, "type": "sub", "expr": "15 - 6", "answer": "9", "userAnswer": ""},
        ]
    },
    # ===== 含 choices 的题型（渲染为按钮）=====
    {
        "name": "compare",
        "title": "比大小",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "compare", "expr": "8 ○ 11", "answer": "＜", "userAnswer": "",
             "choices": ["＞", "＝", "＜"]},
            {"id": 2, "type": "compare", "expr": "15 + 3 ○ 18", "answer": "＝", "userAnswer": "",
             "choices": ["＞", "＝", "＜"]},
            {"id": 3, "type": "compare", "expr": "20 - 5 ○ 12", "answer": "＞", "userAnswer": "",
             "choices": ["＞", "＝", "＜"]},
            {"id": 4, "type": "compare", "expr": "7 ○ 7", "answer": "＝", "userAnswer": "",
             "choices": ["＞", "＝", "＜"]},
            {"id": 5, "type": "compare", "expr": "13 + 4 ○ 16", "answer": "＞", "userAnswer": "",
             "choices": ["＞", "＝", "＜"]},
        ]
    },
    {
        "name": "fillOp",
        "title": "填运算符",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "fillOp", "expr": "14 ○ 6 = 8", "answer": "-", "userAnswer": "",
             "choices": ["+", "-"]},
            {"id": 2, "type": "fillOp", "expr": "3 ○ 7 = 10", "answer": "+", "userAnswer": "",
             "choices": ["+", "-"]},
            {"id": 3, "type": "fillOp", "expr": "12 ○ 5 = 7", "answer": "-", "userAnswer": "",
             "choices": ["+", "-"]},
            {"id": 4, "type": "fillOp", "expr": "9 ○ 8 = 17", "answer": "+", "userAnswer": "",
             "choices": ["+", "-"]},
        ]
    },
    # ===== 填空类（expr 含 __）=====
    {
        "name": "fill",
        "title": "填空练习",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "fill", "expr": "__ + 5 = 12", "answer": "7", "userAnswer": ""},
            {"id": 2, "type": "fill", "expr": "13 - __ = 8", "answer": "5", "userAnswer": ""},
            {"id": 3, "type": "fill", "expr": "6 + __ = 15", "answer": "9", "userAnswer": ""},
            {"id": 4, "type": "fill", "expr": "__ - 4 = 9", "answer": "13", "userAnswer": ""},
        ]
    },
    {
        "name": "multFill",
        "title": "乘法填空",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "multFill", "expr": "3 × __ = 12", "answer": "4", "userAnswer": ""},
            {"id": 2, "type": "multFill", "expr": "__ × 5 = 20", "answer": "4", "userAnswer": ""},
            {"id": 3, "type": "multFill", "expr": "6 × __ = 18", "answer": "3", "userAnswer": ""},
            {"id": 4, "type": "multFill", "expr": "__ × 7 = 21", "answer": "3", "userAnswer": ""},
        ]
    },
    {
        "name": "pattern",
        "title": "找规律",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "pattern", "expr": "2 , 4 , __ , 8 , 10", "answer": "6", "userAnswer": ""},
            {"id": 2, "type": "pattern", "expr": "5 , 10 , 15 , __ , 25", "answer": "20", "userAnswer": ""},
            {"id": 3, "type": "pattern", "expr": "1 , 3 , 5 , __ , 9", "answer": "7", "userAnswer": ""},
        ]
    },
    # ===== 其他数学题型 =====
    {
        "name": "chain",
        "title": "连加连减",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "chain", "expr": "3 + 5 + 2", "answer": "10", "userAnswer": ""},
            {"id": 2, "type": "chain", "expr": "15 - 4 - 3", "answer": "8", "userAnswer": ""},
            {"id": 3, "type": "chain", "expr": "7 + 6 + 2", "answer": "15", "userAnswer": ""},
            {"id": 4, "type": "chain", "expr": "20 - 6 - 5", "answer": "9", "userAnswer": ""},
        ]
    },
    {
        "name": "mulT",
        "title": "表内乘法",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "mulT", "expr": "3 × 4", "answer": "12", "userAnswer": ""},
            {"id": 2, "type": "mulT", "expr": "6 × 7", "answer": "42", "userAnswer": ""},
            {"id": 3, "type": "mulT", "expr": "8 × 9", "answer": "72", "userAnswer": ""},
            {"id": 4, "type": "mulT", "expr": "5 × 6", "answer": "30", "userAnswer": ""},
            {"id": 5, "type": "mulT", "expr": "7 × 8", "answer": "56", "userAnswer": ""},
            {"id": 6, "type": "mulT", "expr": "9 × 9", "answer": "81", "userAnswer": ""},
            {"id": 7, "type": "mulT", "expr": "2 × 7", "answer": "14", "userAnswer": ""},
            {"id": 8, "type": "mulT", "expr": "4 × 6", "answer": "24", "userAnswer": ""},
        ]
    },
    {
        "name": "sameAdd",
        "title": "同数连加",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "sameAdd", "expr": "3 + 3 + 3", "answer": "9", "userAnswer": ""},
            {"id": 2, "type": "sameAdd", "expr": "5 + 5 + 5", "answer": "15", "userAnswer": ""},
            {"id": 3, "type": "sameAdd", "expr": "4 + 4", "answer": "8", "userAnswer": ""},
            {"id": 4, "type": "sameAdd", "expr": "2 + 2 + 2 + 2", "answer": "8", "userAnswer": ""},
        ]
    },
    {
        "name": "parenMix",
        "title": "括号混合",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "parenMix", "expr": "15 - (3 + 4)", "answer": "8", "userAnswer": ""},
            {"id": 2, "type": "parenMix", "expr": "10 + (8 - 5)", "answer": "13", "userAnswer": ""},
            {"id": 3, "type": "parenMix", "expr": "(6 + 3) - 4", "answer": "5", "userAnswer": ""},
            {"id": 4, "type": "parenMix", "expr": "20 - (12 - 7)", "answer": "15", "userAnswer": ""},
        ]
    },
    {
        "name": "vertical",
        "title": "竖式计算",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "vertical", "expr": "36 + 47", "answer": "83", "userAnswer": ""},
            {"id": 2, "type": "vertical", "expr": "72 - 38", "answer": "34", "userAnswer": ""},
            {"id": 3, "type": "vertical", "expr": "45 + 29", "answer": "74", "userAnswer": ""},
            {"id": 4, "type": "vertical", "expr": "81 - 56", "answer": "25", "userAnswer": ""},
        ]
    },
    # ===== 图形类 =====
    {
        "name": "hundredChart",
        "title": "百数表填空",
        "subject": "math",
        "questions": [
            {
                "id": 1, "type": "hundredChart",
                "expr": '{"rows":3,"cols":3,"cellMap":{"0,0":"23","0,1":"24","0,2":"25","1,0":"33","1,2":"35","2,0":"43","2,1":"44","2,2":"45"},"centerKey":"1,1","hiddenKeys":["1,1"]}',
                "answer": "34", "userAnswer": ""
            }
        ]
    },
    {
        "name": "triangle",
        "title": "三角形填数",
        "subject": "math",
        "questions": [
            {
                "id": 1, "type": "triangle",
                "expr": '{"target":10,"vals":{"A":1,"B":2,"C":3,"AB":7,"BC":5,"AC":6},"shown":["A","B","C"],"hidden":["AB","BC","AC"]}',
                "answer": "7,5,6", "userAnswer": ""
            }
        ]
    },
    {
        "name": "square",
        "title": "方形填数",
        "subject": "math",
        "questions": [
            {
                "id": 1, "type": "square",
                "expr": '{"target":10,"vals":{"A":1,"B":2,"C":3,"D":4,"AB":7,"BC":5,"CD":3,"DA":5},"shown":["A","B","C","D"],"hidden":["AB","BC","CD","DA"]}',
                "answer": "7,5,3,5", "userAnswer": ""
            }
        ]
    },
    # ===== 语文 =====
    {
        "name": "pinyin",
        "title": "看拼音写汉字",
        "subject": "chinese",
        "questions": [
            {"id": 1, "type": "pinyin", "char": "思", "pinyin": "sī",
             "answer": "思", "userAnswer": "",
             "choices": ["思", "田", "丝", "想"]},
            {"id": 2, "type": "pinyin", "char": "床", "pinyin": "chuáng",
             "answer": "床", "userAnswer": "",
             "choices": ["床", "庄", "窗", "广"]},
            {"id": 3, "type": "pinyin", "char": "前", "pinyin": "qián",
             "answer": "前", "userAnswer": "",
             "choices": ["前", "月", "钱", "后"]},
            {"id": 4, "type": "pinyin", "char": "明", "pinyin": "míng",
             "answer": "明", "userAnswer": "",
             "choices": ["明", "名", "鸣", "冥"]},
        ]
    },
    # ===== 英语 =====
    {
        "name": "word",
        "title": "英语单词",
        "subject": "english",
        "questions": [
            {"id": 1, "type": "word", "word": "apple", "zh": "苹果", "emoji": "🍎",
             "answer": "apple", "userAnswer": "",
             "choices": ["apple", "banana", "orange", "grape"]},
            {"id": 2, "type": "word", "word": "dog", "zh": "狗", "emoji": "🐕",
             "answer": "dog", "userAnswer": "",
             "choices": ["dog", "cat", "bird", "fish"]},
            {"id": 3, "type": "word", "word": "sun", "zh": "太阳", "emoji": "☀️",
             "answer": "sun", "userAnswer": "",
             "choices": ["sun", "moon", "star", "cloud"]},
            {"id": 4, "type": "word", "word": "cat", "zh": "猫", "emoji": "🐱",
             "answer": "cat", "userAnswer": "",
             "choices": ["cat", "dog", "pig", "cow"]},
        ]
    },
    # ===== 应用题 =====
    {
        "name": "generic",
        "title": "应用题",
        "subject": "math",
        "questions": [
            {"id": 1, "type": "generic", "prompt": "小明有 5 个苹果，又买了 3 个，一共有几个苹果？",
             "answer": "8", "userAnswer": ""},
            {"id": 2, "type": "generic", "prompt": "树上原来有 12 只鸟，飞走了 4 只，还剩几只？",
             "answer": "8", "userAnswer": ""},
            {"id": 3, "type": "generic", "prompt": "一盒铅笔有 6 支，小华买了 2 盒，一共有几支铅笔？",
             "answer": "12", "userAnswer": ""},
        ]
    },
]


def main():
    template_content = TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(exist_ok=True)

    for case in TEST_CASES:
        q_data = {
            "title": case["title"],
            "subject": case["subject"],
            "questions": case["questions"]
        }
        q_data_json = json.dumps(q_data, ensure_ascii=False, indent=2)

        pattern = r'const QUESTION_DATA = \{.*?\};\s*\n'
        replacement = f'const QUESTION_DATA = {q_data_json};\n'
        new_content = re.sub(pattern, replacement, template_content, count=1, flags=re.DOTALL)

        if new_content == template_content:
            print(f"[WARN] {case['name']}: 未找到 QUESTION_DATA 替换位置")
            continue

        output_path = OUTPUT_DIR / f"{case['name']}.html"
        output_path.write_text(new_content, encoding="utf-8")
        print(f"[OK] {case['name']}: {len(case['questions'])} 题 → {output_path.name}")

    print(f"\n共生成 {len(list(OUTPUT_DIR.glob('*.html')))} 个测试文件 → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
