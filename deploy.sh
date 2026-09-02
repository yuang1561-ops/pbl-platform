#!/bin/bash
# PBL 导师工作台一键部署脚本
# 用法: ./deploy.sh [--skip-build]
# 流程: 本地构建 → git提交推送 → 打包 → 上传服务器 → 解压 → 重启 → 验证

set -e
SERVER_HOST="114.215.177.33"
SERVER_PASS="Gaoyuan112!"
REMOTE_DIR="/opt/pbl-platform"
STATIC_DIR="/opt/pbl-static"
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
SSHPASS="$SERVER_PASS" sshpass -e scp -o StrictHostKeyChecking=no "$PACKAGE" root@"$SERVER_HOST":/tmp/

# 5. 服务器部署
echo "▶ [5/6] 服务器解压 + 重启..."
SSHPASS="$SERVER_PASS" sshpass -e ssh -o StrictHostKeyChecking=no root@"$SERVER_HOST" 'bash -s' << 'REMOTE'
set -e
rm -rf /tmp/pbl-upd && mkdir -p /tmp/pbl-upd
tar xzf /tmp/pbl-deploy.tar.gz -C /tmp/pbl-upd 2>/dev/null || true
# 后端代码
cp -r /tmp/pbl-upd/backend/app/* /opt/pbl-platform/backend/app/ 2>/dev/null || true
# 课件
[ -d /tmp/pbl-upd/courses ] && rm -rf /opt/pbl-platform/courses && cp -r /tmp/pbl-upd/courses /opt/pbl-platform/courses
# 知识库
[ -f /tmp/pbl-upd/data/kb.db ] && cp /tmp/pbl-upd/data/kb.db /opt/pbl-platform/data/kb.db
# 前端静态
[ -d /tmp/pbl-upd/frontend/dist ] && rm -rf /opt/pbl-static/pbl && cp -r /tmp/pbl-upd/frontend/dist /opt/pbl-static/pbl
# 权限
find /opt/pbl-static -type f -exec chmod 644 {} + 2>/dev/null || true
find /opt/pbl-static -type d -exec chmod 755 {} + 2>/dev/null || true
find /opt/pbl-platform -type f -exec chmod 644 {} + 2>/dev/null || true
# 重启
systemctl restart pbl-platform
sleep 2
echo "REMOTE_DONE"
REMOTE

# 6. 验证
echo "▶ [6/6] 线上验证..."
curl -s https://www.jinsi.group/pbl-api/health
echo ""
curl -s -o /dev/null -w "知识库页面: HTTP %{http_code}\n" https://www.jinsi.group/pbl/knowledge
echo "════════ 部署完成 ════════"
