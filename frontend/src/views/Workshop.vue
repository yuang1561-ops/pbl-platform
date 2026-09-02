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
        <el-step title="课程详设" description="目标/评价/资源" />
        <el-step title="完整预览" description="方案书 + 导出" />
      </el-steps>

      <!-- 当前步骤用到的方法提示（轻量，不占空间） -->
      <div class="method-tip" v-if="stepMethod">
        <span class="method-label">📘 本步方法：</span>
        <span class="method-text">{{ stepMethod }}</span>
        <span class="method-note">填写内容将在最后一步生成工具卡</span>
      </div>

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
        <div class="ai-gen">
          <el-button type="primary" plain :loading="intentLoading" @click="aiIntent" :disabled="!form.audience && !form.scene">
            🤖 AI 提炼意图声明
          </el-button>
          <span class="ai-hint" v-if="!form.audience && !form.scene">（先填①②，AI 帮你写③）</span>
        </div>
        <el-alert v-if="intentResult" type="success" :closable="false" class="ai-result-box">
          <div class="ai-result-text">{{ intentResult }}</div>
          <el-button size="small" type="primary" link @click="form.intent = intentResult; intentResult = ''">采用</el-button>
        </el-alert>
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

        <div class="ai-gen">
          <el-button type="primary" plain :loading="aiLoading" @click="aiGenerate" :disabled="!form.intent && !form.driving_question">
            🤖 AI 生成候选问题
          </el-button>
          <span class="ai-hint" v-if="!form.intent">（建议先填第 1 步「意图」，生成更精准）</span>
        </div>
        <div v-if="aiQuestions.length" class="ai-results">
          <div v-for="(q, i) in aiQuestions" :key="i" class="ai-item" @click="useAiQuestion(q)">
            <span class="ai-num">Q{{ i + 1 }}</span>
            <span class="ai-text">{{ q }}</span>
            <el-tag size="small" type="success" effect="light" class="ai-use">选用 →</el-tag>
          </div>
          <p class="ai-note">点击任一问题即填入上方输入框，可继续修改</p>
        </div>

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
        <div class="ai-gen">
          <el-button type="primary" plain :loading="elementsLoading" @click="aiElements" :disabled="!form.driving_question">
            🤖 AI 建议五要素（自动填充）
          </el-button>
          <span class="ai-hint">基于意图+驱动问题生成建议，可逐项修改</span>
        </div>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" @click="next">下一步</el-button>
        </div>
      </div>

      <!-- 第 4 步：课程详设 -->
      <div v-else-if="step === 4" class="step-body">
        <h3>📐 课程详设</h3>
        <p class="step-tip">目的：把方案做厚——补全学习目标、评价方案、资源需求与实施计划，让课程可直接执行。</p>
        <el-form label-position="top">
          <el-row :gutter="16">
            <el-col :span="24">
              <el-form-item label="学习目标（知识 / 技能 / 素养，用分号隔开）">
                <el-input type="textarea" :rows="3" v-model="form.objectives" placeholder="知识：了解布达佩斯与多瑙河文明；技能：学会策展与导览表达；素养：跨文化理解与协作" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="评价方案（形成性 + 终结性，怎么评、何时评）">
                <el-input type="textarea" :rows="3" v-model="form.evaluation_detail" placeholder="形成性：每阶段结束用评价矩阵自评互评；终结性：结营面向真实观众导览，用展示评价表" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="资源需求（场地 / 物料 / 人员 / 合作方）">
                <el-input type="textarea" :rows="3" v-model="form.resources" placeholder="场地：杭州博物馆展厅；物料：展签卡/评价表/讲解设备；人员：1 主讲 + 2 助教；合作：馆方讲解员" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="实施计划（阶段编辑器：每阶段 = 名称 / 时间 / 核心活动 / 学生产出 / 教师动作）">
                <div class="phases-editor">
                  <div v-for="(ph, pi) in form.phases" :key="pi" class="phase-card">
                    <div class="phase-head">
                      <span class="phase-num">阶段 {{ pi + 1 }}</span>
                      <el-button size="small" type="danger" link @click="removePhase(pi)">删除</el-button>
                    </div>
                    <el-row :gutter="10">
                      <el-col :span="16"><el-input v-model="ph.name" size="small" placeholder="阶段名称，如：策展启蒙" /></el-col>
                      <el-col :span="8"><el-input v-model="ph.time" size="small" placeholder="时间，如：1课时/40分钟" /></el-col>
                    </el-row>
                    <el-input class="phase-act" v-model="ph.activities" type="textarea" :rows="2" size="small"
                      placeholder="核心活动（每步用分号隔开）：入项游戏；分组选题；确定驱动问题" />
                    <el-row :gutter="10">
                      <el-col :span="12"><el-input v-model="ph.output" size="small" placeholder="学生产出，如：选题卡" /></el-col>
                      <el-col :span="12"><el-input v-model="ph.teacher" size="small" placeholder="教师动作，如：引导讨论/提供资料" /></el-col>
                    </el-row>
                  </div>
                  <el-button type="primary" plain size="small" @click="addPhase">＋ 添加阶段</el-button>
                </div>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <div class="ai-gen">
          <el-button type="primary" plain :loading="detailLoading" @click="aiDetail">🤖 AI 一键补全详设</el-button>
          <el-button type="primary" plain :loading="planLoading" @click="aiPlan">🤖 AI 生成阶段计划</el-button>
          <span class="ai-hint">AI 根据前面信息自动生成学习目标/评价/资源/分阶段计划</span>
        </div>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" @click="next">下一步：完整预览 →</el-button>
        </div>
      </div>

      <!-- 第 5 步：完整方案预览 -->
      <div v-else-if="step === 5" class="step-body">
        <h3>📖 完整方案预览</h3>
        <p class="step-tip">目的：以方案书形式预览整门课，确认后导出 Word / 打印 / 存入项目库。</p>

        <div class="doc-preview">
          <div class="doc-title">PBL 研学课程方案</div>
          <div class="doc-meta">
            <span v-if="form.audience">对象：{{ form.audience }}</span>
            <span v-if="form.duration">时长：{{ form.duration }}</span>
            <span v-if="form.scene">场景：{{ form.scene }}</span>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">一、课程意图</div>
            <p>{{ form.intent || '（待补充）' }}</p>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">二、驱动性问题（项目的心脏）</div>
            <div class="doc-driving-block">💡 {{ form.driving_question || '（待补充）' }}</div>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">三、立项要素</div>
            <table class="doc-table">
              <tr><td class="td-lbl">成果产出</td><td>{{ form.product || '—' }}</td></tr>
              <tr><td class="td-lbl">评估方式</td><td>{{ form.evaluation || '—' }}</td></tr>
            </table>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">四、学习目标</div>
            <p>{{ form.objectives || '（待补充）' }}</p>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">五、评价方案</div>
            <p>{{ form.evaluation_detail || '（待补充）' }}</p>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">六、资源需求</div>
            <p>{{ form.resources || '（待补充）' }}</p>
          </div>

          <div class="doc-sec">
            <div class="doc-sec-title">七、实施计划</div>
            <div v-if="form.phases.length" class="plan-table-wrap">
              <table class="plan-table">
                <tr><th style="width:12%">阶段</th><th style="width:14%">时间</th><th>核心活动</th><th style="width:16%">学生产出</th><th style="width:16%">教师动作</th></tr>
                <tr v-for="(ph, pi) in form.phases" :key="pi">
                  <td class="td-ph">{{ ph.name || ('阶段' + (pi+1)) }}</td>
                  <td>{{ ph.time || '—' }}</td>
                  <td>{{ ph.activities || '—' }}</td>
                  <td>{{ ph.output || '—' }}</td>
                  <td>{{ ph.teacher || '—' }}</td>
                </tr>
              </table>
            </div>
            <div v-else class="doc-plan">{{ form.plan || '（待补充）' }}</div>
          </div>
        </div>

        <div class="toolkit-gen">
          <el-button type="warning" size="large" @click="openToolkit">
            🛠️ 生成课程工具包（本课工具卡）
          </el-button>
        </div>
        <div class="step-actions">
          <el-button @click="prev">上一步</el-button>
          <el-button type="primary" :loading="exporting" @click="exportDoc">📄 导出详细 Word 方案</el-button>
          <el-button type="success" :loading="saving" @click="openSaveDialog">存入项目库</el-button>
          <el-button @click="reset">重新开始</el-button>
        </div>
      </div>
    </el-card>

    <!-- 工具卡原文弹窗 -->
    <el-dialog v-model="toolcardOpen" :title="'📖 本步工具卡（' + stepToolcards.length + '）'" width="680px" top="5vh">
      <div v-for="t in stepToolcards" :key="t.id" class="tc-card">
        <div class="tc-head">
          <span class="tc-name">{{ t.name }}</span>
          <span class="tc-desc">{{ t.desc }}</span>
          <el-button size="small" link type="primary" @click="printToolcard(t)">🖨️ 打印</el-button>
        </div>
        <pre class="tc-content">{{ t.content }}</pre>
      </div>
    </el-dialog>

    <!-- 课程工具包预览弹窗 -->
    <el-dialog v-model="toolkitOpen" title="🛠️ 课程配套工具（可直接用于教学）" width="800px" top="4vh" class="toolkit-dialog">
      <div v-for="(card, ci) in toolkit" :key="ci" class="tk-card">
        <div class="tk-head">
          <span class="tk-icon">{{ card.icon }}</span>
          <div>
            <div class="tk-name">{{ card.name }}</div>
            <div class="tk-desc">{{ card.desc }}</div>
          </div>
        </div>
        <div v-if="card.note" class="tk-note">{{ card.note }}</div>
        <div v-if="card.rows">
          <div v-for="(r, ri) in card.rows" :key="ri" class="tk-row">
            <span class="tk-lbl">{{ r.label }}</span>
            <span class="tk-val" :class="{ highlight: r.highlight }">{{ r.value }}</span>
          </div>
          <div v-if="card.objectives && card.objectives.length" class="tk-obj">
            <div v-for="(o, oi) in card.objectives" :key="oi" class="tk-obj-row">
              <span class="obj-tag">{{ o.k }}</span>
              <span class="obj-val">{{ o.v }}</span>
            </div>
          </div>
          <div v-if="card.checklist" class="tk-ck">
            <span v-for="(c, i) in card.checklist" :key="i" class="ck-item" :class="{ on: c.checked }">
              {{ c.checked ? '✅' : '⬜' }} {{ c.label }}
            </span>
          </div>
        </div>
        <div v-if="card.grid" class="tk-grid">
          <div v-for="(g, gi) in card.grid" :key="gi" class="tk-gitem">
            <div class="g-lbl">{{ g.label }}</div>
            <div class="g-val">{{ g.value }}</div>
          </div>
        </div>
        <table v-if="card.planCols" class="tk-table">
          <tr>
            <th v-for="(c, ci) in card.planCols" :key="ci" :style="ci === 0 ? 'width:14%' : (ci === 1 ? 'width:13%' : '')">{{ c }}</th>
          </tr>
          <tr v-for="(pl, pi) in card.planRows" :key="pi">
            <td class="tk-phase">{{ pl.name }}</td>
            <td>{{ pl.time }}</td>
            <td>{{ pl.activities }}</td>
            <td>{{ pl.output }}</td>
            <td>{{ pl.teacher }}</td>
          </tr>
        </table>
      </div>
      <template #footer>
        <el-button @click="toolkitOpen = false">关闭</el-button>
        <el-button type="primary" @click="printToolkit">🖨️ 打印工具包</el-button>
      </template>
    </el-dialog>

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
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { get, post, saveWorkshop, loadWorkshop } from '../api'
import { buildToolkit } from '../toolkit'

const step = ref(0)
const templates = ref([])
const exporting = ref(false)
const saving = ref(false)
const saveDialog = ref(false)
const aiLoading = ref(false)
const aiQuestions = ref([])
const toolkit = ref([])
const toolkitOpen = ref(false)

// 每步使用的方法说明（最后一步生成工具卡）
const STEP_METHOD = {
  1: 'PBL 目标体系 · 确定课程意图与学习目标',
  2: '核心驱动问题设计卡 · 撰写与检验驱动性问题',
  3: '立项五要素画布 · 定清项目全貌',
  4: '评价矩阵 · 设计学习目标与评价方案',
  5: '确认方案内容 · 导出 Word / 打印 / 存入项目库',
}
const stepMethod = computed(() => STEP_METHOD[step.value] || '')
const intentLoading = ref(false)
const intentResult = ref('')
const elementsLoading = ref(false)
const planLoading = ref(false)
const detailLoading = ref(false)
const saveForm = ref({ title: '', driving_q: '', product: '' })

const form = ref({
  template_id: '', intent: '', driving_question: '', audience: '',
  age: '', duration: '', scene: '', product: '', evaluation: '', plan: '',
  objectives: '', evaluation_detail: '', resources: '',
  phases: []
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
  form.value.objectives = '知识：' + t.title + '核心知识；技能：观察探究与表达；素养：协作与责任感'
  form.value.evaluation_detail = '形成性：过程评价矩阵（自评+互评）；终结性：' + (t.product || '成果展示') + ' 展示评价'
  form.value.resources = '场地：' + (t.scene || '杭州') + '；物料：学习单/评价表/展示材料'
  form.value.plan = ''
  form.value.phases = []
}

const next = () => { if (step.value < 5) { step.value++; saveWorkshop(form.value) } }
const prev = () => { step.value-- }
const reset = () => {
  step.value = 0
  form.value = { template_id: '', intent: '', driving_question: '', audience: '', age: '', duration: '', scene: '', product: '', evaluation: '', plan: '', objectives: '', evaluation_detail: '', resources: '', phases: [] }
  saveWorkshop(form.value)
}

async function aiIntent() {
  intentLoading.value = true
  intentResult.value = ''
  try {
    const d = await post('/workshop/ai', { action: 'intent', audience: form.value.audience, scene: form.value.scene })
    if (d.ok) intentResult.value = d.result
    else ElMessage.error('AI 生成失败：' + (d.error || ''))
  } catch (e) { ElMessage.error('AI 生成失败：' + e.message) }
  intentLoading.value = false
}

async function aiElements() {
  elementsLoading.value = true
  try {
    const d = await post('/workshop/ai', {
      action: 'elements', intent: form.value.intent, driving_question: form.value.driving_question, audience: form.value.audience
    })
    if (d.ok && d.result) {
      const r = d.result
      if (r.age) form.value.age = r.age
      if (r.duration) form.value.duration = r.duration
      if (r.scene) form.value.scene = r.scene
      if (r.product) form.value.product = r.product
      if (r.evaluation) form.value.evaluation = r.evaluation
      ElMessage.success('五要素已自动填充，可修改')
    } else ElMessage.error('AI 生成失败：' + (d.error || ''))
  } catch (e) { ElMessage.error('AI 生成失败：' + e.message) }
  elementsLoading.value = false
}

function addPhase() {
  form.value.phases.push({ name: '', time: '', activities: '', output: '', teacher: '' })
}

function removePhase(i) {
  form.value.phases.splice(i, 1)
}

// 解析 AI 文本或旧 plan 文本 → phases 数组
function parsePlanToPhases(text) {
  if (!text) return
  const phases = []
  text.split(/\n|｜/).forEach(line => {
    line = line.trim()
    if (!line) return
    const m = line.match(/^第?[一二三四五六0-9]+阶段\s*[：:]?\s*(.+?)(?:（约?(.+?)）)?$/)
    const content = m ? m[1] : line
    const time = m && m[2] ? m[2] : ''
    // 拆活动（分号/顿号分隔）
    const parts = content.split(/[；;]/).map(s => s.trim()).filter(s => s)
    const name = parts[0] || content
    const acts = parts.slice(1).join('；')
    phases.push({ name, time, activities: acts, output: '', teacher: '' })
  })
  if (phases.length) form.value.phases = phases
}

async function aiDetail() {
  detailLoading.value = true
  try {
    const d = await post('/workshop/ai', {
      action: 'detail', intent: form.value.intent, driving_question: form.value.driving_question,
      audience: form.value.audience, age: form.value.age, duration: form.value.duration,
      scene: form.value.scene, product: form.value.product, evaluation: form.value.evaluation
    })
    if (d.ok && d.result) {
      const r = d.result
      if (r.objectives) form.value.objectives = r.objectives
      if (r.evaluation_detail) form.value.evaluation_detail = r.evaluation_detail
      if (r.resources) form.value.resources = r.resources
      ElMessage.success('详设已生成，可修改')
    } else ElMessage.error('AI 生成失败：' + (d.error || ''))
  } catch (e) { ElMessage.error('AI 生成失败：' + e.message) }
  detailLoading.value = false
}

async function aiPlan() {
  planLoading.value = true
  try {
    const d = await post('/workshop/ai', {
      action: 'plan', intent: form.value.intent, driving_question: form.value.driving_question,
      audience: form.value.audience, duration: form.value.duration, product: form.value.product
    })
    if (d.ok) {
      if (Array.isArray(d.result)) {
        // 后端已结构化：直接填入阶段编辑器
        form.value.phases = d.result.map(ph => ({
          name: ph.name || '', time: ph.time || '',
          activities: ph.activities || '', output: ph.output || '', teacher: ph.teacher || ''
        }))
        form.value.plan = d.result.map((ph, i) => `第${i+1}阶段 ${ph.name}（${ph.time}）：${ph.activities}；产出：${ph.output}`).join('\n')
      } else {
        form.value.plan = d.result
        parsePlanToPhases(d.result)
      }
      ElMessage.success('阶段计划已生成并填入表格，可修改')
    } else ElMessage.error('AI 生成失败：' + (d.error || ''))
  } catch (e) { ElMessage.error('AI 生成失败：' + e.message) }
  planLoading.value = false
}

async function aiGenerate() {
  aiLoading.value = true
  aiQuestions.value = []
  try {
    const d = await post('/workshop/ai-questions', {
      intent: form.value.intent,
      audience: form.value.audience,
      scene: form.value.scene,
      count: 3
    })
    if (d.ok) {
      aiQuestions.value = d.questions
      if (!d.questions.length) ElMessage.warning('AI 没有返回结果，请重试')
    } else {
      ElMessage.error('AI 生成失败：' + (d.error || '未知错误'))
    }
  } catch (e) {
    ElMessage.error('AI 生成失败：' + e.message)
  }
  aiLoading.value = false
}

function useAiQuestion(q) {
  form.value.driving_question = q
  ElMessage.success('已填入，可继续修改')
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

function openToolkit() {
  toolkit.value = buildToolkit(form.value)
  toolkitOpen.value = true
}

function printToolcard(t) {
  const w = window.open('', '_blank')
  w.document.write(`<html><head><title>${t.name}</title>
    <style>body{font-family:"PingFang SC",sans-serif;padding:32px;line-height:1.8}
    h1{font-size:22px}h2{font-size:17px;margin-top:24px}pre{white-space:pre-wrap;font-family:inherit;font-size:14px}</style></head>
    <body><h1>${t.name}</h1><p style="color:#666">${t.desc}</p><pre>${t.content.replace(/</g,'&lt;')}</pre>
    <script>window.onload=()=>window.print()</scr${'ipt'}></body></html>`)
  w.document.close()
}

function printToolkit() {
  const t = toolkit.value
  let html = `<html><head><title>PBL 课程工具包</title>
    <style>body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;padding:40px;line-height:1.7;color:#222}
    h1{font-size:24px;border-bottom:3px solid #409eff;padding-bottom:10px}
    .card{border:1px solid #dcdfe6;border-radius:10px;padding:18px 22px;margin:18px 0;page-break-inside:avoid}
    .card h2{font-size:18px;margin:0 0 4px}.card .d{color:#666;font-size:13px;margin:0 0 12px}
    .row{display:flex;border-bottom:1px dashed #ebeef5;padding:8px 0}.row:last-child{border:none}
    .lbl{width:180px;color:#666;font-weight:600;flex-shrink:0}.val{flex:1}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px}
    .g-item{border:1px solid #ebeef5;border-radius:6px;padding:8px 12px}
    .g-lbl{font-size:12px;color:#909399}.g-val{font-size:14px;margin-top:2px}
    .ck{color:#67c23a;font-size:13px;margin:3px 0}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border:1px solid #dcdfe6;padding:8px 12px;text-align:left;font-size:14px}
    th{background:#f5f7fa}</style></head><body>`
  html += `<h1>PBL 课程工具包</h1><p style="color:#666">${new Date().toLocaleString('zh-CN')} · 由项目工坊生成</p>`
  t.forEach(card => {
    html += `<div class="card"><h2>${card.icon} ${card.name}</h2><p class="d">${card.desc}</p>`
    if (card.rows) {
      card.rows.forEach(r => {
        html += `<div class="row"><div class="lbl">${r.label}</div><div class="val"${r.highlight ? ' style="font-weight:700;color:#409eff"' : ''}>${(r.value || '').replace(/</g,'&lt;')}</div></div>`
      })
      if (card.checklist) {
        card.checklist.forEach(c => html += `<div class="ck">${c.checked ? '☑' : '☐'} ${c.label}${c.tip ? '（' + c.tip + '）' : ''}</div>`)
      }
      if (card.note) {
        html += `<div style="margin:8px 0;padding:6px 12px;background:#fdf6ec;border-left:3px solid #e6a23c;border-radius:5px;font-size:13px;color:#e6a23c">${card.note.replace(/</g,'&lt;')}</div>`
      }
    }
    if (card.objectives && card.objectives.length) {
      html += `<div style="margin:8px 0">`
      card.objectives.forEach(o => html += `<div style="padding:4px 10px;background:#f0f9eb;border-radius:5px;margin:3px 0"><b style="color:#67c23a">${o.k}</b>：${o.v.replace(/</g,'&lt;')}</div>`)
      html += `</div>`
    }
    if (card.grid) {
      html += `<div class="grid">`
      card.grid.forEach(g => html += `<div class="g-item"><div class="g-lbl">${g.label}</div><div class="g-val">${(g.value || '').replace(/</g,'&lt;')}</div></div>`)
      html += `</div>`
    }
    if (card.planCols) {
      html += `<table><tr>${card.planCols.map(c => '<th>' + c + '</th>').join('')}</tr>`
      card.planRows.forEach(pl => {
        html += `<tr><td><b>${(pl.name||'').replace(/</g,'&lt;')}</b></td><td>${(pl.time||'').replace(/</g,'&lt;')}</td><td>${(pl.activities||'').replace(/</g,'&lt;')}</td><td>${(pl.output||'').replace(/</g,'&lt;')}</td><td>${(pl.teacher||'').replace(/</g,'&lt;')}</td></tr>`
      })
      html += `</table>`
    }
    html += `</div>`
  })
  html += `<script>window.onload=()=>window.print()</scr${'ipt'}></body></html>`
  const w = window.open('', '_blank')
  w.document.write(html)
  w.document.close()
}

onMounted(async () => {
  const d = await get('/templates')
  templates.value = d.templates
  const saved = loadWorkshop()
  if (saved) {
    // 合并默认字段，防止旧草稿缺新字段（phases/objectives 等）
    const defaults = {
      template_id: '', intent: '', driving_question: '', audience: '',
      age: '', duration: '', scene: '', product: '', evaluation: '', plan: '',
      objectives: '', evaluation_detail: '', resources: '', phases: []
    }
    form.value = { ...defaults, ...saved }
    if (!Array.isArray(form.value.phases)) form.value.phases = []
  }
  try { const td = await get('/tools'); toolcardData.value = td.tools } catch (e) {}
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
.method-tip { margin: 14px 0 6px; background: #f0f9eb; border: 1px solid #e1f3d8; border-radius: 8px; padding: 10px 16px; display: flex; align-items: center; gap: 8px; font-size: 13px; }
.method-label { font-weight: 600; color: #67c23a; }
.method-text { color: #303133; }
.method-note { margin-left: auto; color: #c0c4cc; font-size: 12px; }
.phases-editor { width: 100%; }
.phase-card { border: 1px solid #e4e7ed; border-radius: 8px; padding: 10px 12px; margin-bottom: 10px; background: #fafbfc; }
.phase-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.phase-num { font-weight: 700; color: #409eff; font-size: 13px; }
.phase-act { margin: 6px 0; }
.phase-act :deep(textarea) { font-size: 13px; }
.doc-preview { background: #fff; border: 1px solid #e4e7ed; border-radius: 10px; padding: 32px 40px; text-align: left; max-width: 760px; margin: 0 auto; }
.doc-title { font-size: 24px; font-weight: 800; text-align: center; border-bottom: 3px solid #409eff; padding-bottom: 12px; margin-bottom: 10px; }
.doc-meta { text-align: center; color: #909399; font-size: 13px; display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; margin-bottom: 20px; }
.doc-sec { margin: 18px 0; }
.doc-sec-title { font-weight: 700; font-size: 16px; color: #303133; margin-bottom: 6px; border-left: 3px solid #409eff; padding-left: 10px; }
.doc-sec p { margin: 0; line-height: 1.8; color: #444; white-space: pre-wrap; }
.doc-driving-block { font-size: 17px; font-weight: 700; color: #0f3d6b; background: #ecf5ff; border: 1px solid #b3d8ff; border-radius: 8px; padding: 14px 18px; line-height: 1.7; }
.doc-table { width: 100%; border-collapse: collapse; }
.doc-table td { border: 1px solid #e4e7ed; padding: 8px 14px; font-size: 14px; }
.td-lbl { width: 110px; background: #f5f7fa; font-weight: 600; color: #606266; }
.doc-plan { white-space: pre-wrap; line-height: 1.8; }
.plan-table-wrap { overflow-x: auto; }
.plan-table { width: 100%; border-collapse: collapse; }
.plan-table th, .plan-table td { border: 1px solid #e4e7ed; padding: 8px 10px; font-size: 13px; text-align: left; vertical-align: top; line-height: 1.6; }
.plan-table th { background: #f5f7fa; font-weight: 600; }
.td-ph { font-weight: 600; color: #409eff; }
.tc-card { border: 1px solid #e4e7ed; border-radius: 8px; margin-bottom: 14px; overflow: hidden; }
.tc-head { display: flex; align-items: center; gap: 10px; background: #f5f7fa; padding: 10px 16px; border-bottom: 1px solid #e4e7ed; }
.tc-name { font-weight: 700; white-space: nowrap; }
.tc-desc { color: #909399; font-size: 12px; flex: 1; }
.tc-content { white-space: pre-wrap; word-wrap: break-word; font-family: inherit; font-size: 13px; line-height: 1.7; padding: 12px 16px; max-height: 400px; overflow-y: auto; margin: 0; color: #303133; }
.toolkit-gen { margin: 16px 0; text-align: center; background: #fdf6ec; border: 1px dashed #e6a23c; border-radius: 10px; padding: 16px; }
.toolkit-hint { color: #909399; font-size: 12px; margin: 8px 0 0; }
.tk-card { border: 1px solid #e4e7ed; border-radius: 10px; margin-bottom: 14px; overflow: hidden; }
.tk-head { display: flex; gap: 10px; align-items: center; background: #f5f7fa; padding: 12px 16px; border-bottom: 1px solid #e4e7ed; }
.tk-icon { font-size: 22px; }
.tk-name { font-weight: 700; }
.tk-desc { font-size: 12px; color: #909399; }
.tk-note { font-size: 12px; color: #e6a23c; background: #fdf6ec; border-left: 3px solid #e6a23c; padding: 6px 12px; border-radius: 5px; margin: 8px 16px; }
.tk-row { display: flex; padding: 8px 16px; border-bottom: 1px dashed #f0f0f0; font-size: 14px; }
.tk-row:last-of-type { border-bottom: none; }
.tk-lbl { width: 170px; color: #909399; flex-shrink: 0; }
.tk-val { flex: 1; }
.tk-val.highlight { font-weight: 700; color: #409eff; }
.tk-ck { display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 16px; }
.ck-item { font-size: 12px; color: #c0c4cc; background: #f5f7fa; border-radius: 4px; padding: 3px 8px; }
.ck-item.on { color: #67c23a; background: #f0f9eb; }
.tk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; padding: 12px 16px; }
.tk-gitem { border: 1px solid #ebeef5; border-radius: 8px; padding: 8px 12px; background: #fafbfc; }
.g-lbl { font-size: 12px; color: #909399; }
.g-val { font-size: 14px; margin-top: 2px; }
.tk-obj { display: flex; flex-direction: column; gap: 4px; padding: 4px 16px 8px; }
.tk-obj-row { display: flex; gap: 10px; font-size: 13px; background: #f0f9eb; border-radius: 5px; padding: 4px 10px; }
.obj-tag { color: #67c23a; font-weight: 600; flex-shrink: 0; min-width: 44px; }
.obj-val { color: #444; }
.tk-table { width: calc(100% - 32px); margin: 10px 16px 14px; border-collapse: collapse; }
.tk-table th, .tk-table td { border: 1px solid #e4e7ed; padding: 6px 9px; font-size: 12.5px; text-align: left; vertical-align: top; line-height: 1.55; }
.tk-table th { background: #f5f7fa; }
.tk-phase { font-weight: 600; color: #409eff; }
.tk-table th, .tk-table td { border: 1px solid #e4e7ed; padding: 7px 12px; font-size: 13px; text-align: left; }
.tk-table th { background: #f5f7fa; }
.ai-gen { margin: 12px 0; display: flex; align-items: center; gap: 10px; }
.ai-result-box { margin: 10px 0; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.ai-result-text { flex: 1; font-size: 14px; line-height: 1.6; }
.ai-hint { font-size: 12px; color: #c0c4cc; }
.ai-results { margin: 12px 0; }
.ai-item { display: flex; align-items: center; gap: 10px; border: 1px solid #dcdfe6; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; cursor: pointer; transition: all .2s; background: #fff; }
.ai-item:hover { border-color: #67c23a; background: #f0f9eb; }
.ai-num { font-weight: 700; color: #67c23a; font-size: 13px; flex-shrink: 0; }
.ai-text { font-size: 14px; line-height: 1.6; flex: 1; }
.ai-use { flex-shrink: 0; }
.ai-note { font-size: 12px; color: #c0c4cc; margin: 4px 0 0; }
.preview { background: #f8f9fb; border: 1px dashed #dcdfe6; border-radius: 8px; padding: 16px; margin-top: 10px; }
.preview h4 { margin: 0 0 10px; }
.pv-item { font-size: 14px; margin-bottom: 6px; }
</style>
