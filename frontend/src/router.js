import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('./views/Home.vue'), meta: { title: '首页' } },
  { path: '/academy', component: () => import('./views/Academy.vue'), meta: { title: '培训学院' } },
  { path: '/academy/:courseId', component: () => import('./views/CourseDetail.vue'), meta: { title: '课程详情' } },
  { path: '/knowledge', component: () => import('./views/Knowledge.vue'), meta: { title: '知识库' } },
  { path: '/workshop', component: () => import('./views/Workshop.vue'), meta: { title: '项目工坊' } },
  { path: '/templates', component: () => import('./views/Templates.vue'), meta: { title: '项目库' } },
]

const router = createRouter({ history: createWebHistory('/pbl/'), routes })
router.afterEach((to) => {
  document.title = to.meta.title + ' · PBL 导师工作台'
  // 简单埋点（fire-and-forget）
  try {
    const courseId = to.params.courseId || ''
    fetch('/pbl-api/stats/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ page: to.path, course_id: courseId }),
      keepalive: true
    }).catch(() => {})
  } catch (e) {}
})
export default router
