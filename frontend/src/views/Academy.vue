<template>
  <div>
    <div class="page-head">
      <h2>培训学院</h2>
      <p>32 课系统课件 · 6 大学习模块 · 从认知到线上 PBL · 学完即可用工坊实战</p>
    </div>

    <el-collapse v-model="activeModules" v-loading="loading">
      <el-collapse-item v-for="m in modules" :key="m.id" :name="m.id">
        <template #title>
          <div class="module-title">
            <span class="module-name">{{ m.name }}</span>
            <el-tag size="small" type="info" class="module-count">{{ m.courses.length }} 课</el-tag>
            <span class="module-desc">{{ m.desc }}</span>
          </div>
        </template>
        <div class="course-grid">
          <div v-for="c in m.courses" :key="c.id" class="course-card" @click="$router.push('/academy/' + c.id)">
            <div class="course-order">{{ c.order }}</div>
            <div class="course-info">
              <div class="course-title">{{ c.title }}</div>
              <div class="course-objective">{{ c.objective || '（待补充学习目标）' }}</div>
              <div class="course-meta">
                <span>约 {{ (c.chars / 1000).toFixed(1) }}K 字</span>
                <span class="done-tag" v-if="progress[c.id]?.finished">✅ 已学完</span>
                <span class="doing-tag" v-else-if="progress[c.id]?.quizzes">📖 学习中</span>
              </div>
            </div>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get, loadProgress } from '../api'

const modules = ref([])
const loading = ref(true)
const activeModules = ref([])
const progress = ref({})

onMounted(async () => {
  const d = await get('/courses')
  modules.value = d.modules
  activeModules.value = d.modules.map(m => m.id)
  // 读所有课程进度
  d.modules.forEach(m => m.courses.forEach(c => {
    const p = loadProgress(c.id)
    if (p && Object.keys(p).length) progress.value[c.id] = p
  }))
  loading.value = false
})
</script>

<style scoped>
.page-head h2 { margin: 0 0 4px; }
.page-head p { color: #909399; margin: 0 0 16px; font-size: 13px; }
.module-title { display: flex; align-items: center; gap: 10px; width: 100%; }
.module-name { font-weight: 600; }
.module-desc { color: #909399; font-size: 12px; margin-left: 6px; }
.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 12px; padding: 4px 8px 8px; }
.course-card { display: flex; gap: 12px; padding: 14px; border: 1px solid #ebeef5; border-radius: 8px; cursor: pointer; transition: all .2s; background: #fff; }
.course-card:hover { border-color: #409eff; box-shadow: 0 2px 12px rgba(64,158,255,.15); transform: translateY(-1px); }
.course-order { font-size: 20px; font-weight: 800; color: #409eff; min-width: 34px; text-align: center; }
.course-title { font-weight: 600; margin-bottom: 4px; }
.course-objective { color: #606266; font-size: 12px; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.course-meta { margin-top: 6px; font-size: 12px; color: #c0c4cc; display: flex; gap: 8px; }
.done-tag { color: #67c23a; }
.doing-tag { color: #e6a23c; }
</style>
