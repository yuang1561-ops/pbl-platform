<template>
  <div>
    <div class="page-head">
      <h2>项目工坊</h2>
      <p>5 步向导设计 PBL 研学课程 —— 每一步都知道目的和产出，30 分钟出 Word 方案</p>
    </div>

    <el-card shadow="never" class="workshop-card">
      <el-steps :active="step" finish-status="success" align-center class="steps">
        <el-step title="选起点" description="模板 or 空白" />
        <el-step title="定义意图" description="为什么做" />
        <el-step title="驱动性问题" description="项目的心脏" />
        <el-step title="立项五要素" description="画布" />
        <el-step title="生成方案" description="导出 Word" />
      </el-steps>

      <!-- 第 0 步：选起点 -->
      <div v-if="step === 0" class="step-body">
        <h3>🎯 选择起点</h3>
        <p class="step-tip">目的：不重复造轮子。从真实课程模板开始，或从空白开始。</p>
        <div class="template-list">
          <div v-for="t in templates" :key="t.id" class="template-opt" :class="{ active: form.template_id === t.id }"
            @click="form.template_id = t.id; fillFromTemplate(t)">
            <div class="t-title">{{ t.title }}</div>
            <div class="t-q">{{ t.driving_q }}</div>
          </div>
          <div class="template-opt" :class="{ active: form.template_id === 'blank' }"
            @click="form.template_id = 'blank'; form.intent=''; form.driving_question=''; form.audience=''; form.age=''; form.duration=''; form.scene=''; form.product=''; form.evaluation=''; form.plan=''">
            <div class="t-title">✨ 从空白开始</div>
            <div class="t-q">自由设计一门全新的 PBL 课程</div>
          </div>
        </div>
        <div class="step-actions">
          <el-button type="primary" @click="next" :disabled="!form.template_id">下一步</el-button>
        </div>
      </div>

      <!-- 第 1 步：定义意图 -->
      <div v-else-if="step === 1" class="step-body">
        <h3>💭 定义意图（为什么做这门课）</h3>
        <p class="step-tip">目的：先定意图再定形式。呼应「鸟屋→工匠」案例——问清楚你真正希望学生带走什么。</p>
        <el-form label-position="top">
          <el-form-item label="① 这门课给谁？（对象）">
            <el-input v-model="form.audience" placeholder="如：小学 4-6 年级研学团" />
          </el-form-item>
          <el-form-item label="② 解决什么真实问题？">
            <el-input v-model="form.scene" placeholder="如：孩子逛博物馆只看热闹，看完就忘" />
          </el-form-item>
          <el-form-item label="③ 希望学生带走什么能力？（意图声明）">
            <el-input type="textarea" :rows="3" v-model="form.intent" placeholder="如：让学生成为主动的观察者与表达者，学会用策展思维讲述文物故事" />
          </el-form-item>
        </el-form>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" @click="next">下一步</el-button>
        </div>
      </div>

      <!-- 第 2 步：驱动性问题 -->
      <div v-else-if="step === 2" class="step-body">
        <h3>❓ 设计驱动性问题（项目的心脏）</h3>
        <p class="step-tip">目的：把挑战变成一个需要解决的问题。好问题的 4 个标准：重要有意义 / 真实关联 / 开放有挑战 / 可持续探究。</p>
        <el-form label-position="top">
          <el-form-item label="你的驱动性问题">
            <el-input type="textarea" :rows="3" v-model="form.driving_question" placeholder="如：如何为一件文物设计一场展览，让同龄人愿意来看？" />
          </el-form-item>
        </el-form>
        <el-alert type="info" :closable="false" title="提示">
          不要用「什么」类问题（教科书式）；不要是「是/否」就能回答；要本地化、具体化。卡住时用公式：我们作为【谁】，为【谁】做【什么】，为了【什么目的】？
        </el-alert>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" @click="next">下一步</el-button>
        </div>
      </div>

      <!-- 第 3 步：立项五要素 -->
      <div v-else-if="step === 3" class="step-body">
        <h3>📋 立项五要素</h3>
        <p class="step-tip">目的：把项目定下来——谁、多久、在哪、产出什么、怎么评。产出：完整立项画布。</p>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="适用年龄"><el-input v-model="form.age" placeholder="如：8-12 岁" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="时长"><el-input v-model="form.duration" placeholder="如：半天 / 3 小时" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="场景"><el-input v-model="form.scene" placeholder="如：杭州博物馆 / 西湖 / 良渚博物院" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="成果产出"><el-input v-model="form.product" placeholder="如：迷你策展方案 + 讲解词" /></el-form-item></el-col>
          <el-col :span="24"><el-form-item label="评估方式"><el-input v-model="form.evaluation" placeholder="如：评价矩阵（过程 + 成果）" /></el-form-item></el-col>
        </el-row>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" @click="next">下一步</el-button>
        </div>
      </div>

      <!-- 第 4 步：生成方案 -->
      <div v-else-if="step === 4" class="step-body">
        <h3>📄 生成课程方案</h3>
        <p class="step-tip">目的：把前 4 步组装成可编辑的 Word 课程方案。可补充实施计划后导出。</p>
        <el-form label-position="top">
          <el-form-item label="实施计划（阶段 / 任务 / 里程碑，可补充）">
            <el-input type="textarea" :rows="5" v-model="form.plan" placeholder="如：第一阶段 入项+选题（1课时）｜第二阶段 研究文物（2课时）｜第三阶段 策展与展示（2课时）" />
          </el-form-item>
        </el-form>
        <div class="preview">
          <h4>方案预览</h4>
          <div class="pv-item"><b>意图：</b>{{ form.intent || '（待补充）' }}</div>
          <div class="pv-item"><b>驱动性问题：</b>{{ form.driving_question || '（待补充）' }}</div>
          <div class="pv-item"><b>受众：</b>{{ form.audience || '—' }} ｜ <b>年龄：</b>{{ form.age || '—' }} ｜ <b>时长：</b>{{ form.duration || '—' }}</div>
          <div class="pv-item"><b>场景：</b>{{ form.scene || '—' }} ｜ <b>成果：</b>{{ form.product || '—' }}</div>
          <div class="pv-item"><b>评估：</b>{{ form.evaluation || '—' }}</div>
        </div>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" :loading="exporting" @click="exportDoc">导出 Word 方案</el-button>
          <el-button type="success" :loading="saving" @click="openSaveDialog">存入项目库</el-button>
          <el-button @click="reset">重新开始</el-button>
        </div>
      </div>
    </el-card>

    <el-dialog v-model="saveDialog" title="存入项目库" width="480px">
      <el-form label-position="top">
        <el-form-item label="模板名称">
          <el-input v-model="saveForm.title" placeholder="如：布达佩斯展·跨时空对话" />
        </el-form-item>
        <el-form-item label="驱动性问题（自动带入，可改）">
          <el-input type="textarea" :rows="2" v-model="saveForm.driving_q" />
        </el-form-item>
        <el-form-item label="成果产出">
          <el-input v-model="saveForm.product" placeholder="如：策展方案 + 讲解词" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="saveDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveTemplate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { get, post, saveWorkshop, loadWorkshop } from '../api'

const step = ref(0)
const templates = ref([])
const exporting = ref(false)
const saving = ref(false)
const saveDialog = ref(false)
const saveForm = ref({ title: '', driving_q: '', product: '' })

const form = ref({
  template_id: '', intent: '', driving_question: '', audience: '',
  age: '', duration: '', scene: '', product: '', evaluation: '', plan: ''
})

function fillFromTemplate(t) {
  form.value.intent = `让学生通过「${t.title}」主题项目，获得真实的探究与表达能力`
  form.value.driving_question = t.driving_q
  form.value.audience = t.age + ' 研学团'
  form.value.age = t.age
  form.value.duration = t.duration
  form.value.scene = t.scene || '杭州'
  form.value.product = t.product
  form.value.evaluation = '评价矩阵（过程 + 成果展示）'
  form.value.plan = ''
}

const next = () => { step.value++; saveWorkshop(form.value) }
const prev = () => { step.value-- }
const reset = () => {
  step.value = 0
  form.value = { template_id: '', intent: '', driving_question: '', audience: '', age: '', duration: '', scene: '', product: '', evaluation: '', plan: '' }
  saveWorkshop(form.value)
}

function openSaveDialog() {
  saveForm.value = {
    title: (form.value.scene || '研学') + '·' + (form.value.driving_question || '').slice(0, 12),
    driving_q: form.value.driving_question,
    product: form.value.product,
  }
  saveDialog.value = true
}

async function saveTemplate() {
  if (!saveForm.value.title.trim() || !saveForm.value.driving_q.trim()) {
    ElMessage.warning('模板名称和驱动性问题必填')
    return
  }
  saving.value = true
  try {
    await post('/templates/save', {
      title: saveForm.value.title,
      age: form.value.age,
      duration: form.value.duration,
      driving_q: saveForm.value.driving_q,
      product: saveForm.value.product,
      scene: form.value.scene,
    })
    ElMessage.success('已存入项目库，可在「项目库」页复用')
    saveDialog.value = false
  } catch (e) {
    ElMessage.error('保存失败：' + e.message)
  }
  saving.value = false
}

async function exportDoc() {
  exporting.value = true
  try {
    const res = await post('/workshop/export', form.value)
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'PBL研学课程方案.docx'
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('课程方案已导出')
  } catch (e) {
    ElMessage.error('导出失败：' + e.message)
  }
  exporting.value = false
}

onMounted(async () => {
  const d = await get('/templates')
  templates.value = d.templates
  const saved = loadWorkshop()
  if (saved) form.value = saved
})
</script>

<style scoped>
.page-head h2 { margin: 0 0 4px; }
.page-head p { color: #909399; margin: 0 0 16px; font-size: 13px; }
.workshop-card { max-width: 980px; }
.steps { margin: 10px 0 30px; }
.step-body { max-width: 800px; margin: 0 auto; }
.step-tip { color: #909399; font-size: 13px; background: #f5f7fa; padding: 10px 14px; border-radius: 6px; }
.template-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 10px; margin: 16px 0; }
.template-opt { border: 1px solid #dcdfe6; border-radius: 8px; padding: 12px; cursor: pointer; transition: all .2s; background: #fff; }
.template-opt:hover, .template-opt.active { border-color: #409eff; box-shadow: 0 2px 8px rgba(64,158,255,.2); }
.t-title { font-weight: 600; margin-bottom: 4px; }
.t-q { font-size: 12px; color: #909399; line-height: 1.5; }
.step-actions { margin-top: 24px; display: flex; gap: 10px; }
.preview { background: #f8f9fb; border: 1px dashed #dcdfe6; border-radius: 8px; padding: 16px; margin-top: 10px; }
.preview h4 { margin: 0 0 10px; }
.pv-item { font-size: 14px; margin-bottom: 6px; }
</style>
