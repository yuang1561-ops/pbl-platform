<template>
  <div>
    <el-card class="hero" shadow="never">
      <h1>PBL 导师工作台</h1>
      <p>浸思研学的 PBL 课程开发与导师赋能平台 —— 学方法论、查资料库、设计课程，一站式完成。</p>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="$router.push('/academy')">开始学习</el-button>
        <el-button size="large" @click="$router.push('/workshop')">进入工坊</el-button>
      </div>
    </el-card>

    <el-row :gutter="16" class="stats">
      <el-col :span="6" v-for="s in stats" :key="s.label">
        <el-card shadow="never" class="stat-card">
          <div class="stat-num">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card v-if="usage" shadow="never" class="usage-card">
      <div class="usage-title">📊 平台使用情况</div>
      <div class="usage-grid">
        <div class="usage-item"><span class="u-num">{{ usage.views }}</span><span class="u-label">累计访问</span></div>
        <div class="usage-item"><span class="u-num">{{ usage.today }}</span><span class="u-label">今日访问</span></div>
        <div class="usage-item"><span class="u-num">{{ usage.feedback.total }}</span><span class="u-label">课程反馈</span></div>
        <div class="usage-item"><span class="u-num">{{ usage.pages }}</span><span class="u-label">访问页面数</span></div>
      </div>
      <div v-if="usage.hot_courses.length" class="hot-list">
        <span class="hot-title">最热课程：</span>
        <el-tag v-for="h in usage.hot_courses" :key="h.id" size="small" type="warning" effect="light" class="hot-tag"
          @click="$router.push('/academy/' + h.id)">{{ h.id }} ({{ h.count }})</el-tag>
      </div>
    </el-card>

    <el-row :gutter="16" class="cards">
      <el-col :span="6" v-for="c in features" :key="c.title">
        <el-card shadow="hover" class="feature-card" @click="$router.push(c.path)">
          <div class="feature-icon">{{ c.icon }}</div>
          <h3>{{ c.title }}</h3>
          <p>{{ c.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get } from '../api'

const usage = ref(null)
onMounted(async () => {
  try { usage.value = await get('/stats') } catch (e) {}
})

const stats = [
  { value: '33', label: '系统课件' },
  { value: '6', label: '学习模块' },
  { value: '2077', label: '知识库页数' },
  { value: '6+', label: '项目模板' },
]

const features = [
  { icon: '📚', title: '培训学院', desc: '33 课系统课件：6 大模块从认知到线上 PBL，带自测与进度', path: '/academy' },
  { icon: '📖', title: '知识库', desc: '9 本 PBL 专著 2077 页全文检索，按主题浏览', path: '/knowledge' },
  { icon: '🛠️', title: '项目工坊', desc: '5 步向导设计课程，30 分钟产出 Word 课程方案', path: '/workshop' },
  { icon: '🗂️', title: '项目库', desc: '真实课程模板，一键复用，从模板开始新项目', path: '/templates' },
]
</script>

<style scoped>
.hero { background: linear-gradient(135deg, #1f2d3d, #2b4a6f); color: #fff; border: none; }
.hero h1 { font-size: 32px; margin: 8px 0; }
.hero p { color: #cfd8e3; font-size: 15px; margin-bottom: 20px; }
.stats { margin-top: 20px; }
.usage-card { margin-top: 20px; max-width: 1200px; }
.usage-title { font-weight: 600; margin-bottom: 12px; }
.usage-grid { display: flex; gap: 40px; }
.usage-item { display: flex; flex-direction: column; }
.u-num { font-size: 26px; font-weight: 800; color: #303133; }
.u-label { font-size: 12px; color: #909399; }
.hot-list { margin-top: 12px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.hot-title { font-size: 13px; color: #606266; }
.hot-tag { cursor: pointer; }
.stat-card { text-align: center; padding: 8px 0; }
.stat-num { font-size: 32px; font-weight: 800; color: #409eff; }
.stat-label { color: #909399; font-size: 13px; margin-top: 4px; }
.cards { margin-top: 20px; }
.feature-card { cursor: pointer; text-align: center; }
.feature-icon { font-size: 38px; margin: 8px 0; }
.feature-card h3 { margin: 10px 0 6px; }
.feature-card p { color: #909399; font-size: 13px; line-height: 1.6; }
</style>
