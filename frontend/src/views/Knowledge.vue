<template>
  <div>
    <div class="page-head">
      <h2>知识库</h2>
      <p>9 本 PBL 专著 · 2077 页全文检索 · 随时查阅，支持回查原书页码</p>
    </div>

    <div class="search-bar">
      <el-input v-model="query" size="large" placeholder="搜索关键词，如：驱动性问题、评价矩阵、团队冲突…" clearable
        @keyup.enter="doSearch" @clear="results = []">
        <template #append>
          <el-button @click="doSearch">搜索</el-button>
        </template>
      </el-input>
      <div class="topic-tags">
        <el-tag v-for="t in topics" :key="t.name" :type="activeTopic === t.name ? 'primary' : 'info'"
          effect="light" class="topic-tag" @click="toggleTopic(t.name)">
          {{ t.name }} ({{ t.count }})
        </el-tag>
      </div>
    </div>

    <div v-loading="loading" class="results">
      <el-empty v-if="!loading && searched && results.length === 0" description="未找到相关结果，换个关键词试试" />
      <div v-for="(r, i) in results" :key="i" class="result-item">
        <div class="result-head">
          <span class="result-title">{{ r.title }}</span>
          <el-tag size="small" v-if="r.topic" type="warning" effect="light">{{ r.topic }}</el-tag>
          <span class="result-page">第 {{ r.page }} 页</span>
        </div>
        <div class="result-snippet" v-html="r.snippet"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { get } from '../api'

const route = useRoute()
const query = ref('')
const topics = ref([])
const activeTopic = ref('')
const results = ref([])
const searched = ref(false)
const loading = ref(false)

async function loadTopics() {
  const d = await get('/kb/topics')
  topics.value = d.topics
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

onMounted(async () => {
  await loadTopics()
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
.result-snippet { color: #606266; font-size: 14px; line-height: 1.7; }
</style>
