<template>
  <div v-loading="loading">
    <template v-if="course">
      <div class="crumb">
        <el-button link @click="$router.push('/academy')">← 返回学院</el-button>
        <el-button link @click="markFinished" type="success" v-if="!finished">✅ 标记本课学完</el-button>
        <el-tag v-else type="success" effect="plain">本课已学完</el-tag>
      </div>
      <div class="doc" v-html="renderedHtml"></div>
      <div class="course-nav">
        <el-button v-if="prevCourse" link type="primary" @click="$router.push('/academy/' + prevCourse.id)">
          ← 上一课：{{ prevCourse.title }}
        </el-button>
        <span v-else></span>
        <el-button v-if="nextCourse" link type="primary" @click="$router.push('/academy/' + nextCourse.id)">
          下一课：{{ nextCourse.title }} →
        </el-button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { get, loadProgress, saveProgress } from '../api'
import { enhanceQuiz } from '../quiz'

const route = useRoute()
const course = ref(null)
const loading = ref(true)
const finished = ref(false)

const progress = loadProgress(route.params.courseId)
finished.value = !!progress.finished
const navCourses = ref([])
const prevCourse = ref(null)
const nextCourse = ref(null)

const renderedHtml = computed(() => {
  if (!course.value) return ''
  return marked.parse(course.value.content)
})

// 渲染完成后执行自测交互增强
watch(renderedHtml, async () => {
  await nextTick()
  enhanceQuiz(document.querySelector('.doc'))
})

function markFinished() {
  finished.value = true
  saveProgress(route.params.courseId, { ...progress, finished: true, finishedAt: Date.now() })
}

async function loadNav() {
  const d = await get('/courses/nav')
  navCourses.value = d.courses
  const idx = navCourses.value.findIndex(c => c.id === route.params.courseId)
  if (idx > 0) prevCourse.value = navCourses.value[idx - 1]
  if (idx >= 0 && idx < navCourses.value.length - 1) nextCourse.value = navCourses.value[idx + 1]
}

onMounted(async () => {
  course.value = await get(`/courses/${route.params.courseId}`)
  loadNav()
  loading.value = false
  // 滚动到顶部
  window.scrollTo(0, 0)
})
</script>

<style>
.crumb { margin-bottom: 12px; display: flex; gap: 8px; align-items: center; }
.course-nav { display: flex; justify-content: space-between; margin-top: 20px; max-width: 960px; padding: 0 8px; }
.doc { background: #fff; border-radius: 8px; padding: 32px 40px; line-height: 1.9; font-size: 15px; box-shadow: 0 1px 4px rgba(0,0,0,.06); max-width: 960px; }
@media (max-width: 768px) {
  .doc { max-width: 100%; padding: 18px 14px !important; font-size: 14px; }
  .course-nav { max-width: 100%; }
}
.doc h1 { font-size: 28px; border-bottom: 2px solid #409eff; padding-bottom: 12px; }
.doc h2 { font-size: 21px; margin-top: 32px; border-left: 4px solid #409eff; padding-left: 12px; }
.doc h3 { font-size: 17px; color: #303133; }
.doc blockquote { border-left: 4px solid #e6a23c; background: #fdf6ec; padding: 10px 16px; border-radius: 4px; margin: 16px 0; color: #7a6a4a; }
.doc code { background: #f0f2f5; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
.doc pre { background: #1f2d3d; color: #e6e6e6; padding: 16px; border-radius: 8px; overflow-x: auto; }
.doc pre code { background: none; color: inherit; }
.doc table { border-collapse: collapse; width: 100%; margin: 16px 0; }
.doc th, .doc td { border: 1px solid #e4e7ed; padding: 8px 12px; text-align: left; }
.doc th { background: #f5f7fa; }
.doc details { background: #f8f9fb; border: 1px dashed #dcdfe6; border-radius: 8px; padding: 12px 16px; margin: 12px 0; }
.doc summary { cursor: pointer; font-weight: 600; color: #409eff; }
.doc details p { margin: 10px 0 0; color: #606266; }
.doc a { color: #409eff; }
.doc hr { border: none; border-top: 1px solid #e4e7ed; margin: 24px 0; }
.quiz-option { display: flex; align-items: center; gap: 10px; border: 1px solid #dcdfe6; border-radius: 8px; padding: 10px 14px; margin: 8px 0; cursor: pointer; transition: all .2s; background: #fff; }
.quiz-option:hover { border-color: #409eff; background: #ecf5ff; }
.quiz-option.selected { border-color: #409eff; background: #ecf5ff; box-shadow: 0 2px 8px rgba(64,158,255,.15); }
.quiz-letter { width: 24px; height: 24px; border-radius: 50%; background: #f0f2f5; color: #606266; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0; }
.quiz-option.selected .quiz-letter { background: #409eff; color: #fff; }
.quiz-tip { font-size: 12px; color: #e6a23c; margin: 4px 0 10px; padding-left: 4px; }
</style>
