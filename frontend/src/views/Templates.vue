<template>
  <div>
    <div class="page-head">
      <h2>项目库</h2>
      <p>真实课程模板 · 点击即可在工坊中复用 · 新项目从模板开始而非从零</p>
    </div>

    <div class="tpl-grid" v-loading="loading">
      <el-card v-for="t in templates" :key="t.id" shadow="hover" class="tpl-card">
        <template #header>
          <div class="tpl-head">
            <span class="tpl-title">{{ t.title }}</span>
            <el-tag size="small" :type="t.custom ? 'success' : 'primary'" effect="light">{{ t.module }}</el-tag>
          </div>
        </template>
        <div class="tpl-body">
          <div class="tpl-q">
            <div class="q-label">驱动性问题</div>
            <div class="q-text">{{ t.driving_q }}</div>
          </div>
          <div class="tpl-meta">
            <span>🎂 {{ t.age }}</span>
            <span>⏱️ {{ t.duration }}</span>
          </div>
          <div class="tpl-product">📦 {{ t.product }}</div>
        </div>
        <div class="tpl-foot">
          <el-button type="primary" size="small" @click="useTemplate(t)">以此模板新建 →</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { get, saveWorkshop } from '../api'

const router = useRouter()
const templates = ref([])
const loading = ref(true)

function useTemplate(t) {
  saveWorkshop({
    template_id: t.id,
    intent: `让学生通过「${t.title}」主题项目，获得真实的探究与表达能力`,
    driving_question: t.driving_q,
    audience: t.age + ' 研学团',
    age: t.age,
    duration: t.duration,
    scene: '杭州',
    product: t.product,
    evaluation: '评价矩阵（过程 + 成果展示）',
    plan: '',
    objectives: '', evaluation_detail: '', resources: '', phases: []
  })
  router.push('/workshop')
}

onMounted(async () => {
  const d = await get('/templates')
  templates.value = d.templates
  loading.value = false
})
</script>

<style scoped>
.page-head h2 { margin: 0 0 4px; }
.page-head p { color: #909399; margin: 0 0 16px; font-size: 13px; }
.tpl-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.tpl-title { font-weight: 600; }
.tpl-q { background: #f5f7fa; border-radius: 6px; padding: 10px 12px; margin-bottom: 10px; }
.q-label { font-size: 12px; color: #909399; margin-bottom: 4px; }
.q-text { font-size: 14px; line-height: 1.6; color: #303133; }
.tpl-meta { display: flex; gap: 16px; font-size: 13px; color: #606266; margin-bottom: 6px; }
.tpl-product { font-size: 13px; color: #909399; }
.tpl-foot { margin-top: 14px; text-align: right; }
</style>
