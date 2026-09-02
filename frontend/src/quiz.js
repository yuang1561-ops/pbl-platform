// 自测题交互增强：把判断题/选择题的 A/B 选项变成可点击
// 兼容两种格式：独立段落选项 & 同段落内 \nA. xxx 换行选项
export function enhanceQuiz(rootEl) {
  if (!rootEl) return
  const doc = rootEl

  // 处理「题 2（判断/选择）」标题所在的段落
  const strongs = doc.querySelectorAll('strong')
  strongs.forEach(h => {
    const t = (h.textContent || '').trim()
    if (!/^题\s*\d+（判断|^题\s*\d+（选择/.test(t)) return

    const p = h.closest('p')
    if (!p) return
    // 该段落 innerHTML 是否有 \nA. 结构（同段选项）
    const html = p.innerHTML
    const optionLines = html.split('\n').filter(l => /^[A-D][\.、．]/.test(l.trim()))
    if (optionLines.length < 2) return

    // 拆段：题干保留，选项行转成独立可点击元素
    const lines = html.split('\n')
    const stemHtml = lines.filter(l => !/^[A-D][\.、．]/.test(l.trim())).join('<br>')
    p.innerHTML = stemHtml

    const container = document.createElement('div')
    container.className = 'quiz-options'
    optionLines.forEach(line => {
      const letter = line.trim()[0]
      const text = line.trim().slice(2).trim()
      const opt = document.createElement('div')
      opt.className = 'quiz-option'
      opt.innerHTML = `<span class="quiz-letter">${letter}</span><span class="quiz-text">${text}</span>`
      opt.addEventListener('click', () => {
        container.querySelectorAll('.quiz-option').forEach(w => w.classList.remove('selected'))
        opt.classList.add('selected')
        // 展开最近的答案 details
        let d = opt
        while (d && d.tagName !== 'DETAILS') d = d.nextElementSibling
        if (d && d.tagName === 'DETAILS') d.setAttribute('open', '')
        container.querySelectorAll('.quiz-tip').forEach(x => x.remove())
        const tip = document.createElement('div')
        tip.className = 'quiz-tip'
        tip.textContent = `你选了 ${letter}，已展开参考答案，对照看看。`
        opt.after(tip)
      })
      container.appendChild(opt)
    })
    p.after(container)
  })
}
