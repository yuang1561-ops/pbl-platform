// 知识库阅读器排版清洗 v3
// 处理 PDF OCR 常见问题：碎行、表格碎片、错位、噪点

export function cleanOcrText(text) {
  if (!text) return ''
  let lines = text.split('\n').map(l => l.replace(/\r$/, ''))

  // 1. 行内碎片合并：中文间/字母数字间的孤立空格（"工 具 9" → "工具9"）
  lines = lines.map(l => {
    l = l.replace(/([\u4e00-\u9fff])\s+([\u4e00-\u9fff])/g, '$1$2')
    l = l.replace(/([A-Za-z0-9])\s+([A-Za-z0-9])/g, '$1$2')
    return l
  })

  // 2. 连续碎片组重组：OCR 把词拆成单字/数字行（如 工/具/9）
  //    把连续 <=2 字符的行合并为一组，尝试拼回
  const pass2 = []
  let i = 0
  while (i < lines.length) {
    const t = lines[i].trim()
    const isTiny = t.length > 0 && t.length <= 2 && !/^\d{1,4}$/.test(t)
    if (isTiny) {
      // 收集连续碎片
      let group = t
      let j = i + 1
      while (j < lines.length) {
        const tj = lines[j].trim()
        if (tj.length > 0 && tj.length <= 2 && !/^\d{1,4}$/.test(tj)) {
          group += tj
          j++
        } else break
      }
      // 如果组后面紧跟纯数字（如"9"），也并入
      if (j < lines.length && /^\d{1,3}$/.test(lines[j].trim())) {
        group += lines[j].trim()
        j++
      }
      // 拼回后的词如果合理（含中文），保留；否则原样
      if (/[\u4e00-\u9fff]/.test(group)) {
        pass2.push(group)
      } else {
        pass2.push(t)
      }
      i = j
    } else {
      pass2.push(lines[i])
      i++
    }
  }
  lines = pass2

  // 3. 表格头识别：连续短词行（<=15字、无句读）→ 合并为一行表头
  const isHeaderWord = (t) => {
    if (!t || t.length === 0 || t.length > 15) return false
    if (/^\d+$/.test(t)) return false
    if (/\d$/.test(t)) return false // 以数字结尾是标题
    if (/[。！？；：，、]/.test(t)) return false // 含句读是正文不是表头
    if (/[a-zA-Z]/.test(t) && t.length < 3) return false
    if (/^▎/.test(t)) return false
    return true
  }
  const merged2 = []
  i = 0
  while (i < lines.length) {
    const t = lines[i].trim()
    const group = []
    let j = i
    while (j < lines.length && isHeaderWord(lines[j].trim()) && group.length < 10) {
      group.push(lines[j].trim())
      j++
    }
    // 表头特征：>=3 个短词连续，且后续行是正文（含句读）或结尾
    if (group.length >= 3) {
      merged2.push('▎' + group.join('｜'))
      i = j
    } else {
      merged2.push(lines[i])
      i++
    }
  }
  lines = merged2

  // 4. 合并多余空行
  const out = []
  let blank = 0
  for (const l of lines) {
    if (l.trim() === '') {
      blank++
      if (blank <= 1) out.push('')
    } else {
      blank = 0
      out.push(l)
    }
  }

  // 5. 清理遗留页分隔符
  return out.join('\n')
    .replace(/=====\s*第\s*\d+\s*页\s*=====/g, '')
    .replace(/^\s*$/gm, '')
}
