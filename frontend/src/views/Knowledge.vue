<template>
  <div>
    <div class="page-head">
      <h2>知识库</h2>
      <p>9 本 PBL 专著 · 2077 页全文可检索 · 点击书目直接阅读</p>
    </div>

    <!-- 搜索区 -->
    <div class="search-bar">
      <el-input v-model="query" size="large" placeholder="搜索关键词，如：驱动性问题、评价矩阵、团队冲突…" clearable
        @keyup.enter="doSearch" @clear="showBooks()">
        <template #append>
          <el-button @click="doSearch">搜索</el-button>
        </template>
      </el-input>
      <div class="topic-tags" v-if="!readingBook">
        <el-tag v-for="t in topics" :key="t.name" :type="activeTopic === t.name ? 'primary' : 'info'"
          effect="light" class="topic-tag" @click="toggleTopic(t.name)">
          {{ t.name }} ({{ t.count }})
        </el-tag>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div v-loading="loading" class="results" v-if="searched">
      <el-empty v-if="results.length === 0" description="未找到相关结果，换个关键词试试" />
      <div v-for="(r, i) in results" :key="i" class="result-item">
        <div class="result-head">
          <span class="result-title">{{ r.title }}</span>
          <el-tag size="small" v-if="r.topic" type="warning" effect="light">{{ r.topic }}</el-tag>
          <span class="result-page">第 {{ r.page }} 页</span>
          <el-button link type="primary" size="small" class="read-btn" @click="openBook(r.title, r.page)">阅读此页 →</el-button>
        </div>
        <div class="result-snippet">{{ r.snippet }}</div>
      </div>
      <el-button v-if="results.length" link @click="showBooks()">← 返回书库</el-button>
    </div>

    <!-- 书库浏览（默认） -->
    <div v-else-if="!readingBook" v-loading="loading">
      <div class="book-grid">
        <el-card v-for="b in books" :key="b.title" shadow="hover" class="book-card" @click="openBook(b.title, 1)">
          <div class="book-head">
            <span class="book-icon">📖</span>
            <div class="book-info">
              <div class="book-title">{{ b.title }}</div>
              <div class="book-pages">{{ b.pages }} 页</div>
            </div>
          </div>
          <div class="book-intro">{{ b.intro || '（本书为扫描版 OCR 全文，可检索可阅读）' }}</div>
          <div class="book-cta">开始阅读 →</div>
        </el-card>
      </div>
    </div>

    <!-- 书籍阅读器 -->
    <div v-else class="reader">
      <div class="reader-head">
        <el-button link @click="closeBook()">← 返回书库</el-button>
        <span class="reader-title">{{ readingBook.title }}</span>
        <div class="jump-box">
          <el-input v-model="jumpPage" size="small" placeholder="跳页" class="jump-input" @keyup.enter="doJump" />
          <el-button size="small" @click="doJump">跳</el-button>
        </div>
        <el-pagination small layout="prev, pager, next" :total="readingBook.total_pages" :page-size="1"
          v-model:current-page="readingBook.page" @current-change="loadBookPage" />
      </div>
      <div class="reader-body" v-loading="pageLoading">
        <div class="reader-content">{{ readingBook.content }}</div>
      </div>
      <div class="reader-nav">
        <el-button :disabled="readingBook.page <= 1" @click="readingBook.page--; loadBookPage()">← 上一页</el-button>
        <span class="reader-page-info">第 {{ readingBook.page }} / {{ readingBook.total_pages }} 页</span>
        <el-button :disabled="readingBook.page >= readingBook.total_pages" @click="readingBook.page++; loadBookPage()">下一页 →</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { get } from '../api'
import { cleanOcrText } from '../ocrClean'

const route = useRoute()
const query = ref('')
const topics = ref([])
const activeTopic = ref('')
const results = ref([])
const searched = ref(false)
const loading = ref(false)
const books = ref([])
const readingBook = ref(null)
const pageLoading = ref(false)
const jumpPage = ref('')

async function loadTopics() {
  const d = await get('/kb/topics')
  topics.value = d.topics
}

async function loadBooks() {
  loading.value = true
  const d = await get('/kb/books')
  books.value = d.books
  loading.value = false
}

function toggleTopic(name) {
  activeTopic.value = activeTopic.value === name ? '' : name
  if (query.value) doSearch()
}

async function doSearch() {
  if (!query.value.trim()) return
  loading.value = true
  searched.value = true
  const params = { q: query.value.trim() }
  if (activeTopic.value) params.topic = activeTopic.value
  const d = await get('/kb/search', params)
  results.value = d.results
  loading.value = false
}

function showBooks() {
  searched.value = false
  query.value = ''
  activeTopic.value = ''
}

function openBook(title, page) {
  readingBook.value = { title, page, content: '', total_pages: 1 }
  loadBookPage()
}

async function loadBookPage() {
  if (!readingBook.value) return
  pageLoading.value = true
  const d = await get('/kb/book', { title: readingBook.value.title, page: readingBook.value.page })
  readingBook.value.content = cleanOcrText(d.content)
  readingBook.value.total_pages = d.total_pages
  readingBook.value.page = d.page
  pageLoading.value = false
}

function doJump() {
  const p = parseInt(jumpPage.value)
  if (p >= 1 && p <= readingBook.value.total_pages) {
    readingBook.value.page = p
    loadBookPage()
  }
  jumpPage.value = ''
}

function closeBook() {
  readingBook.value = null
}

onMounted(async () => {
  await loadTopics()
  await loadBooks()
  // 支持从 URL 带 ?q= 进入（课件延伸阅读链接跳转）
  if (route.query.q) {
    query.value = route.query.q
    doSearch()
  }
})
</script>

<style scoped>
.page-head h2 { margin: 0 0 4px; }
.page-head p { color: #909399; margin: 0 0 16px; font-size: 13px; }
.search-bar { max-width: 860px; }
.topic-tags { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }
.topic-tag { cursor: pointer; }
.results { margin-top: 20px; max-width: 860px; }
.result-item { background: #fff; border: 1px solid #ebeef5; border-radius: 8px; padding: 16px 20px; margin-bottom: 10px; }
.result-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.result-title { font-weight: 600; }
.result-page { color: #c0c4cc; font-size: 12px; margin-left: auto; }
.read-btn { margin-left: 4px; }
.result-snippet { color: #606266; font-size: 14px; line-height: 1.7; }

/* 书库网格 */
.book-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; margin-top: 8px; }
.book-card { cursor: pointer; transition: all .2s; }
.book-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.1); }
.book-head { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.book-icon { font-size: 34px; }
.book-title { font-weight: 600; font-size: 15px; line-height: 1.4; }
.book-pages { font-size: 12px; color: #909399; margin-top: 2px; }
.book-intro { color: #606266; font-size: 13px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; min-height: 60px; }
.book-cta { margin-top: 10px; color: #409eff; font-size: 13px; font-weight: 500; }

/* 阅读器 */
.reader { margin-top: 8px; }
.reader-head { display: flex; align-items: center; gap: 16px; background: #fff; border: 1px solid #e4e7ed; border-radius: 8px 8px 0 0; padding: 10px 16px; }
.reader-title { font-weight: 600; flex: 1; }
.jump-box { display: flex; align-items: center; gap: 4px; }
.jump-input { width: 64px; }
.reader-body { background: #fff; border: 1px solid #e4e7ed; border-top: none; padding: 20px 28px; min-height: 50vh; max-height: 65vh; overflow-y: auto; }
.reader-content { white-space: pre-wrap; word-wrap: break-word; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; font-size: 15px; line-height: 1.9; color: #303133; margin: 0; }
.reader-nav { display: flex; align-items: center; justify-content: space-between; background: #fff; border: 1px solid #e4e7ed; border-top: none; border-radius: 0 0 8px 8px; padding: 10px 16px; }
.reader-page-info { color: #909399; font-size: 13px; }
</style>
