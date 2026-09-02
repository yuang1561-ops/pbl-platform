#!/usr/bin/env python3
"""知识库数据准备：9 本书 OCR 全文 → SQLite FTS5"""
import sqlite3, os, re, json

OCR_DIR = "/Users/yuangao/Desktop/PBL项目学习/_ocr_texts"
DB = os.path.join(os.path.dirname(__file__), "..", "..", "data", "kb.db")

BOOKS = [
    ("巴克教师指南", "项目学习教师指南：21世纪的中学教学法  （第二版）教育科学出版社.美国巴克教育研究所著.txt"),
    ("50个工具玩转项目式学习", "_50个工具玩转项目式学习=50 TOOLS FOR PROJECT BASED_15249395.txt"),
    ("项目教学法（凯兹）", "项目教学法-12024259.txt"),
    ("小小探索家", "小小探索家 幼儿教育中的项目课程教学_13746468.txt"),
    ("培养小小探索家", "培养小小探索家——幼儿教育中的项目教学法.txt"),
    ("多元智能与项目学习", "多元智能与项目学习  活动设计指导.txt"),
    ("项目课程的魅力", "项目课程的魅力_11724365.txt"),
    ("PBL行动者手册", "PBL行动者手册.txt"),
    ("PBL行动者手册Vol2幼儿版", "PBL 行动者手册 Vol.2（幼儿版）.txt"),
]

TOPICS = {
    "驱动性问题": ["驱动问题", "驱动性问题", "核心驱动问题"],
    "评估": ["评价", "评估", "评价表", "BESMART", "反思"],
    "团队管理": ["团队", "小组", "冲突", "协作", "合作"],
    "幼儿PBL": ["幼儿", "幼儿园", "学步儿", "瑞吉欧"],
    "线上PBL": ["线上", "在线", "远程", "网络"],
    "多元智能": ["多元智能", "智力", "智能"],
    "课程设计": ["以终为始", "立项", "计划", "课程标准", "项目设计"],
    "项目式思维": ["项目式思维", "思维方式", "设计思维"],
    "案例": ["案例", "项目实例", "课程实录"],
}

def split_pages(text):
    """按页标记切分，返回 [(页码, 内容)]"""
    parts = re.split(r"===== 第(\d+)页 =====", text)
    pages = []
    for i in range(1, len(parts), 2):
        pages.append((int(parts[i]), parts[i+1].strip()))
    return pages

def main():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.execute("CREATE VIRTUAL TABLE books USING fts5(title, topic, page, content, tokenize='trigram')")
    total = 0
    for title, fname in BOOKS:
        path = os.path.join(OCR_DIR, fname)
        if not os.path.exists(path):
            print(f"❌ 缺失: {fname}")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        pages = split_pages(text)
        for page_no, content in pages:
            if len(content) < 30:
                continue
            # 主题标注
            topic = ""
            for tname, kws in TOPICS.items():
                if any(kw in content for kw in kws):
                    topic = tname
                    break
            conn.execute(
                "INSERT INTO books(title, topic, page, content) VALUES (?,?,?,?)",
                (title, topic, page_no, content))
            total += 1
    conn.commit()
    # 统计
    print(f"✅ 知识库入库完成: {total} 页")
    for (title,) in conn.execute("SELECT DISTINCT title FROM books"):
        cnt = conn.execute("SELECT COUNT(*) FROM books WHERE title=?", (title,)).fetchone()[0]
        print(f"  {title}: {cnt} 页")
    # 主题覆盖
    print("\n主题覆盖:")
    for tname, kws in TOPICS.items():
        cnt = conn.execute("SELECT COUNT(*) FROM books WHERE topic=?", (tname,)).fetchone()[0]
        print(f"  {tname}: {cnt} 页")
    conn.close()

if __name__ == "__main__":
    main()
