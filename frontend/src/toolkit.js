// 工坊工具包生成器：把导师在工坊各步填的内容，映射进结构化工具模板
// 每张工具卡 = 一个可视化表格/卡片，字段值来自工坊表单

function inferBeneficiary(form) {
  const s = (form.scene || '') + (form.product || '')
  if (/博物馆|展览|文物|展/.test(s)) return '同龄学生 / 参观者（面向展览观众）'
  if (/西湖|水质|环境|自然/.test(s)) return '社区居民 / 西湖游客'
  if (/丝绸|丝路/.test(s)) return '同龄学生 / 文化爱好者'
  if (/南宋|宋韵/.test(s)) return '同龄学生 / 文化体验者'
  return form.audience ? form.audience + ' 及受益群体' : '（待补充）'
}

export function buildToolkit(form) {
  const tools = []

  // 卡1：PBL 目标体系（来自第1步 意图 + 第4步 学习目标）
  const objParts = []
  const obj = form.objectives || ''
  // objectives 形如 "知识：X；技能：Y；素养：Z"
  if (obj) {
    obj.split(/[；;]/).forEach(s => {
      s = s.trim()
      if (s) objParts.push({ k: s.split(/[：:]/)[0] || '目标', v: s.split(/[：:]/).slice(1).join('：').trim() || s })
    })
  }
  tools.push({
    name: 'PBL 目标体系',
    icon: '🎯',
    desc: '课程目标（来自第 1 步·意图 + 第 4 步·学习目标）',
    rows: [
      { label: '课程意图', value: form.intent || '（待补充）' },
      { label: '目标受众', value: form.audience || '（待补充）' },
      { label: '解决的真实问题', value: form.scene || '（待补充）' },
    ],
    objectives: objParts.length ? objParts : null,
  })

  // 卡2：核心驱动问题设计卡（来自第2步 驱动性问题）
  tools.push({
    name: '核心驱动问题设计卡',
    icon: '❓',
    desc: '项目的心脏（来自第 2 步·驱动性问题）',
    rows: [
      { label: '谁？（项目主体）', value: form.audience || '（待补充）' },
      { label: '为谁？（服务对象）', value: inferBeneficiary(form) },
      { label: '解决什么问题？', value: form.scene || '（待补充）' },
      { label: '驱动性问题（定稿）', value: form.driving_question || '（待补充）', highlight: true },
    ],
    checklist: [
      { label: '有兴趣（学生视角）', checked: !!form.driving_question },
      { label: '有挑战（可完成）', checked: !!form.driving_question },
      { label: '有意义（现实价值）', checked: !!form.driving_question },
    ],
  })

  // 卡3：立项五要素画布（来自第3步 五要素）
  tools.push({
    name: '立项五要素画布',
    icon: '📋',
    desc: '项目全貌一图看（来自第 3 步·立项五要素）',
    grid: [
      { label: '核心驱动问题', value: form.driving_question || '—' },
      { label: '适用年龄', value: form.age || '—' },
      { label: '时长', value: form.duration || '—' },
      { label: '场景', value: form.scene || '—' },
      { label: '成果产出', value: form.product || '—' },
      { label: '评估方式', value: form.evaluation || '—' },
    ],
  })

  // 卡4：实施计划表（来自第4步 结构化 phases）——5 列完整表格
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
