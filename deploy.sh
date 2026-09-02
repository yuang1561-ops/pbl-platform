#!/bin/bash
# PBL 导师工作台一键部署脚本
# 用法: ./deploy.sh [--skip-build]
# 流程: 本地构建 → git提交推送 → 打包 → 上传服务器 → 解压 → 重启 → 验证

set -e
SERVER="root@114.215.177.33"
REMOTE_DIR="/opt/pbl-platform"
STATIC_DIR="/opt/pbl-static"
SSH="sshpass -p 'Gaoyuan112!' ssh -o StrictHostKeyChecking=no"
SCP="sshpass -p 'Gaoyuan112!' scp -o StrictHostKeyChecking=no"
PACKAGE="/tmp/pbl-deploy.tar.gz"

echo "════════ PBL 部署脚本 ════════"

# 1. 构建前端
if [ "$1" != "--skip-build" ]; then
  echo "▶ [1/6] 构建前端..."
  npm --prefix frontend run build 2>&1 | grep -E "built|error" | head -2
fi

# 2. 提交推送 GitHub
echo "▶ [2/6] 提交并推送 GitHub..."
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M') 更新" 2>/dev/null || echo "  （无变更）"
git push origin main 2>&1 | tail -1

# 3. 打包
echo "▶ [3/6] 打包..."
tar czf "$PACKAGE" \
  --exclude='frontend/node_modules' --exclude='frontend/src' --exclude='frontend/public' \
  --exclude='backend/venv' --exclude='*/__pycache__' \
  backend/app frontend/dist courses data docs 2>/dev/null || true

# 4. 上传
echo "▶ [4/6] 上传到服务器..."
eval "$SCP $PACKAGE $SERVER:/tmp/"

# 5. 服务器部署
echo "▶ [5/6] 服务器解压 + 重启..."
eval "$SSH 'rm -rf /tmp/pbl-upd && mkdir -p /tmp/pbl-upd && tar xzf /tmp/pbl-deploy.tar.gz -C /tmp/pbl-upd 2>/dev/null
  cp -r /tmp/pbl-upd/backend/app/* $REMOTE_DIR/backend/app/ 2>/dev/null || true
  [ -d /tmp/pbl-upd/courses ] && rm -rf $REMOTE_DIR/courses && cp -r /tmp/pbl-upd/courses $REMOTE_DIR/courses
  [ -f /tmp/pbl-upd/data/kb.db ] && cp /tmp/pbl-upd/data/kb.db $REMOTE_DIR/data/kb.db
  [ -d /tmp/pbl-upd/frontend/dist ] && rm -rf $STATIC_DIR/pbl && cp -r /tmp/pbl-upd/frontend/dist $STATIC_DIR/pbl
  find $STATIC_DIR -type f -exec chmod 644 {} + 2>/dev/null
  find $STATIC_DIR -type d -exec chmod 755 {} + 2>/dev/null
  find $REMOTE_DIR -type f -exec chmod 644 {} + 2>/dev/null
  systemctl restart pbl-platform
  sleep 2
  echo DONE'"

# 6. 验证
echo "▶ [6/6] 线上验证..."
curl -s https://www.jinsi.group/pbl-api/health
echo ""
curl -s -o /dev/null -w "知识库页面: HTTP %{http_code}\n" https://www.jinsi.group/pbl/knowledge
echo "════════ 部署完成 ════════"
