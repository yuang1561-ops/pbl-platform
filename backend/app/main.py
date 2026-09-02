#!/usr/bin/env python3
"""PBL 导师工作台后端"""
import os, re, json, sqlite3, urllib.parse
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE = Path(__file__).resolve().parent.parent.parent
COURSES_DIR = BASE / "courses"
DB_PATH = BASE / "data" / "kb.db"

app = FastAPI(title="PBL 导师工作台", docs_url="/pbl-api/docs", openapi_url="/pbl-api/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ═══════════════ 课程 API ═══════════════

MODULES = [
    ("module1", "模块 1｜PBL 是什么", "认知建立：为什么是 PBL、探究式 vs 项目式、全景与思维"),
    ("module2", "模块 2｜设计项目", "核心模块：设计师思维、定义挑战、驱动性问题、以终为始、个性化、21 世纪技能、计划设计"),
    ("module3", "模块 3｜管理团队", "实施阶段：培养团队、避免危机、规划进程、构建文化"),
    ("module4", "模块 4｜评估与复盘", "评估成长、用好观众、复盘反思"),
    ("module5", "模块 5｜推进者进阶", "深度学习、思维转变、真实性、协作、创造力、失败原因"),
    ("module6", "模块 6｜线上 PBL", "差异化亮点：线上设计、7 原则、7 策略、协作与社群、评估分享"),
]

def parse_course_meta(path: Path):
    """从课件 md 提取元信息"""
    text = path.read_text(encoding="utf-8")
    title = ""
    m = re.search(r"^# (.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    # 学习目标（兼容 **学习目标**： 和 学习目标： 格式）
    objective = ""
    m = re.search(r"\*\*学习目标\*\*[：:](.+?)(?:\n|$)|学习目标[：:](.+?)(?:\n|$)", text)
    if m:
        objective = (m.group(1) or m.group(2) or "").strip()
    # 字数
    chars = len(re.sub(r"[\s#*`>|-]", "", text))
    return {"title": title, "objective": objective, "chars": chars}

@app.get("/pbl-api/courses/nav")
def course_nav():
    """返回全部课程的有序列表（供上一课/下一课导航）"""
    items = []
    for mod_id, _, _ in MODULES:
        mod_dir = COURSES_DIR / mod_id
        if mod_dir.exists():
            for f in sorted(mod_dir.glob("*.md")):
                meta = parse_course_meta(f)
                items.append({"id": f.stem, "title": meta["title"], "module": mod_id})
    return {"courses": items}

@app.get("/pbl-api/courses")
def list_courses():
    modules = []
    for mod_id, name, desc in MODULES:
        mod_dir = COURSES_DIR / mod_id
        courses = []
        if mod_dir.exists():
            for f in sorted(mod_dir.glob("*.md")):
                meta = parse_course_meta(f)
                course_id = f.stem
                courses.append({
                    "id": course_id,
                    "title": meta["title"],
                    "objective": meta["objective"],
                    "chars": meta["chars"],
                    "order": f.name.split("-")[0],
                })
        modules.append({"id": mod_id, "name": name, "desc": desc, "courses": courses})
    return {"modules": modules}

@app.get("/pbl-api/courses/{course_id}")
def get_course(course_id: str):
    for mod_id, _, _ in MODULES:
        p = COURSES_DIR / mod_id / f"{course_id}.md"
        if p.exists():
            content = p.read_text(encoding="utf-8")
            # 把「知识库检索"XXX"」转成可点击链接（跳转知识库页并自动搜索）
            import html as _html
            def _linkify(m):
                kw = m.group(1)
                href = f"/pbl/knowledge?q={urllib.parse.quote(kw)}"
                return f'<a class="kb-link" href="{href}" target="_blank">知识库检索「{_html.escape(kw)}」</a>'
            content = re.sub(r'知识库检索[“"]([^”"]+)[”"]', _linkify, content)
            return {"id": course_id, "module": mod_id, "content": content}
    return {"error": "not found"}

# ═══════════════ 知识库 API ═══════════════

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/pbl-api/kb/search")
def kb_search(q: str = Query(..., min_length=1), topic: str = "", limit: int = 20):
    conn = get_conn()
    # 转义 FTS5 特殊字符
    esc = re.sub(r'["*()]', ' ', q).strip()
    if not esc:
        return {"results": []}
    sql = "SELECT title, topic, page, snippet(books, -1, '[', ']', '…', 12) AS snip FROM books WHERE books MATCH ?"
    params = [f'"{esc}"']
    if topic:
        sql += " AND topic = ?"
        params.append(topic)
    sql += " LIMIT ?"
    params.append(limit)
    try:
        rows = conn.execute(sql, params).fetchall()
    except Exception:
        # 回退 LIKE 搜索
        like = f"%{q}%"
        sql = "SELECT title, topic, page, substr(content, 1, 200) AS snip FROM books WHERE content LIKE ?"
        params = [like]
        if topic:
            sql += " AND topic = ?"
            params.append(topic)
        sql += " LIMIT ?"
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
    results = [{"title": r["title"], "topic": r["topic"], "page": r["page"], "snippet": r["snip"]} for r in rows]
    conn.close()
    return {"results": results, "total": len(results)}

@app.get("/pbl-api/kb/topics")
def kb_topics():
    conn = get_conn()
    rows = conn.execute("SELECT topic, COUNT(*) as cnt FROM books WHERE topic != '' GROUP BY topic ORDER BY cnt DESC").fetchall()
    conn.close()
    return {"topics": [{"name": r["topic"], "count": r["cnt"]} for r in rows]}

# ═══════════════ 项目库 API ═══════════════

BUILTIN_TEMPLATES = [
        {"id": "hz-museum", "title": "杭博暑期研学·文物会说话", "age": "8-12 岁", "duration": "3 小时",
         "driving_q": "如何为一件文物设计一场展览，让同龄人愿意来看？",
         "product": "迷你策展方案 + 讲解词", "scene": "杭州博物馆", "module": "模块 2 设计项目"},
        {"id": "liangzhu", "title": "良渚博物院·玉器密码", "age": "10-14 岁", "duration": "半天",
         "driving_q": "良渚的玉器为什么能'说话'？请你为一件玉器写一份身份档案。",
         "product": "玉器身份档案 + 讲解", "scene": "良渚博物院", "module": "模块 2 设计项目"},
        {"id": "westlake-water", "title": "西湖水质侦探", "age": "9-12 岁", "duration": "半天",
         "driving_q": "西湖的水质适合鱼类生存吗？我们如何验证并保护它？",
         "product": "水质报告 + 保护建议书", "scene": "西湖", "module": "模块 2 设计项目"},
        {"id": "budapest", "title": "布达佩斯展·跨时空对话", "age": "8-14 岁", "duration": "全天",
         "driving_q": "如果匈牙利文物会说话，它们最想告诉杭州孩子什么？",
         "product": "跨时空对话展览 + 导览", "scene": "杭州博物馆（布达佩斯展）", "module": "模块 6 线上 PBL"},
        {"id": "silk-road", "title": "丝绸之路·杭州出发", "age": "10-15 岁", "duration": "1 天",
         "driving_q": "丝绸如何改变世界？请你设计一条从杭州出发的'新丝绸之路'展线。",
         "product": "展线方案 + 沙盘", "scene": "中国丝绸博物馆", "module": "模块 2 设计项目"},
        {"id": "qiannian-song", "title": "南宋风雅·生活美学", "age": "8-12 岁", "duration": "半天",
         "driving_q": "南宋人怎样把日子过成诗？请你复刻一件南宋生活器物。",
         "product": "器物复刻 + 生活美学手册", "scene": "南宋官窑博物馆", "module": "模块 5 推进者进阶"},
    ]

def _init_template_db():
    conn = get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS custom_templates (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, age TEXT, duration TEXT, driving_q TEXT, product TEXT, scene TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

@app.get("/pbl-api/templates")
def list_templates():
    """项目模板（内置 + 用户自存）"""
    _init_template_db()
    conn = get_conn()
    customs = conn.execute("SELECT * FROM custom_templates ORDER BY id DESC").fetchall()
    conn.close()
    custom_list = [{"id": f"c{t['id']}", "title": t["title"], "age": t["age"], "duration": t["duration"],
                    "driving_q": t["driving_q"], "product": t["product"], "scene": t["scene"],
                    "module": "导师自存", "custom": True} for t in customs]
    return {"templates": BUILTIN_TEMPLATES + custom_list}

class TemplateData(BaseModel):
    title: str
    age: str = ""
    duration: str = ""
    driving_q: str = ""
    product: str = ""
    scene: str = ""

@app.post("/pbl-api/templates/save")
def save_template(data: TemplateData):
    """把工坊产出存为项目模板"""
    _init_template_db()
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO custom_templates(title, age, duration, driving_q, product, scene) VALUES (?,?,?,?,?,?)",
        (data.title, data.age, data.duration, data.driving_q, data.product, data.scene))
    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return {"ok": True, "id": f"c{tid}"}

# ═══════════════ 工坊 API ═══════════════

class WorkshopData(BaseModel):
    template_id: str = ""
    intent: str = ""
    driving_question: str = ""
    audience: str = ""
    age: str = ""
    duration: str = ""
    scene: str = ""
    product: str = ""
    evaluation: str = ""
    plan: str = ""

@app.post("/pbl-api/workshop/export")
def workshop_export(data: WorkshopData):
    """生成课程方案 .docx"""
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()
    # 标题
    title = doc.add_heading("PBL 研学课程方案", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("浸思研学 · PBL 课程开发工坊出品")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    def section(name, content):
        doc.add_heading(name, level=1)
        doc.add_paragraph(content or "（待补充）")

    section("一、课程意图（为什么做这门课）", data.intent)
    section("二、驱动性问题（项目的心脏）", data.driving_question)
    doc.add_heading("三、立项五要素", level=1)
    items = [
        ("目标受众", data.audience),
        ("适用年龄", data.age),
        ("时长", data.duration),
        ("场景", data.scene),
        ("成果产出", data.product),
        ("评估方式", data.evaluation),
    ]
    for k, v in items:
        p = doc.add_paragraph()
        r = p.add_run(f"{k}：")
        r.bold = True
        p.add_run(v or "（待补充）")
    section("四、实施计划", data.plan)

    # 保存到内存返回
    import io
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    from fastapi.responses import Response
    return Response(
        content=buf.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="pbl_course_plan.docx"'}
    )

# ═══════════════ 静态前端 ═══════════════

FRONT_DIST = BASE / "frontend" / "dist"
if FRONT_DIST.exists():
    app.mount("/pbl", StaticFiles(directory=FRONT_DIST, html=True), name="pbl-front")

@app.get("/pbl-api/health")
def health():
    return {"status": "ok", "courses_dir": str(COURSES_DIR), "kb": str(DB_PATH)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8100)
