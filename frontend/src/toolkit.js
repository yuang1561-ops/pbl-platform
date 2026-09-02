// 工坊工具包生成器：配套执行工具（非重复方案信息）
// 4 张卡：驱动问题分解表 / 评价矩阵结构化表 / 三维检验卡 / 实施计划表

export function buildToolkit(form) {
  const tools = []

  // 卡1：驱动问题分解表（AI 生成子问题→任务→产出）
  // 若 phases 有子问题字段则用，否则用 AI decompose 结果（未来）
  const decompRows = form.phases && form.phases.length
    ? form.phases.map((ph, i) => ({
        sub_q: `子问题${i+1}：${ph.name || '阶段' + (i+1)}`,
        task: ph.activities || '—',
        output: ph.output || '—',
        milestone: ph.time || '—'
      }))
    : [{ sub_q: '（待 AI 生成驱动问题分解）', task: '—', output: '—', milestone: '—' }]
  tools.push({
    name: '驱动问题分解表',
    icon: '❓',
    desc: '把核心问题拆成 3-4 个子问题，每个对应任务与产出',
    note: '💡 点击"AI 生成阶段计划"后，此处自动填充分解表',
    decompCols: ['子问题', '核心任务', '学生产出', '里程碑'],
    decompRows: decompRows,
  })

  // 卡2：评价矩阵结构化表（4 列：评价内容/证据/方式/时机）
  const rubricRows = form.evaluation_detail
    ? form.evaluation_detail.split(/[；;]/).map(s => s.trim()).filter(s => s).map(s => {
        const m = s.match(/^(形成性|终结性)[：: ]*(.*)$/)
        if (m) {
          return {
            criterion: m[1] + '评价',
            evidence: m[2].slice(0, 30),
            method: '评价矩阵/展示评价',
            timing: m[1] === '形成性' ? '各阶段结束' : '结营展示'
          }
        }
        return { criterion: s.slice(0, 20), evidence: '—', method: '—', timing: '—' }
      })
    : [{ criterion: '（待补充评价方案）', evidence: '—', method: '—', timing: '—' }]
  tools.push({
    name: '评价矩阵结构化表',
    icon: '📊',
    desc: '把评价方案拆成 4 列可执行表格',
    rubricCols: ['评价内容', '证据', '评价方式', '评价时机'],
    rubricRows: rubricRows,
  })

  // 卡3：驱动问题三维检验卡（自检+改进建议）
  tools.push({
    name: '驱动问题三维检验卡',
    icon: '✅',
    desc: '用三个维度检验驱动性问题质量',
    checklist: [
      { label: '有兴趣（学生视角）', checked: !!form.driving_question, tip: '学生是否觉得"这问题跟我有关"？' },
      { label: '有挑战（可完成）', checked: !!form.driving_question, tip: '难度是否在学生最近发展区内？' },
      { label: '有意义（现实价值）', checked: !!form.driving_question, tip: '解决问题是否有真实受益者？' },
    ],
    note: form.driving_question ? `✅ 你的驱动问题："${form.driving_question.slice(0,40)}${form.driving_question.length>40?'…':''}" 已填入，建议邀请 2-3 位学生试读，收集反馈后微调。` : '⚠️ 请先在第 2 步填写驱动性问题',
  })

  // 卡4：实施计划表（5 列完整表格）
  const hasPhases = Array.isArray(form.phases) && form.phases.length > 0
  tools.push({
    name: '课程实施计划表',
    icon: '🗓️',
    desc: hasPhases ? '分阶段执行计划（来自第 4 步·课程详设）' : '分阶段执行计划',
    planCols: ['阶段', '时间', '核心活动', '学生产出', '教师动作'],
    planRows: hasPhases
      ? form.phases.map((ph, i) => ({
          name: ph.name || '阶段' + (i + 1),
          time: ph.time || '—',
          activities: ph.activities || '—',
          output: ph.output || '—',
          teacher: ph.teacher || '—'
        }))
      : [{ name: '（待补充）', time: '—', activities: '—', output: '—', teacher: '—' }],
  })

  return tools
}
