<template>
    <div class="auth-container">
        <!-- 背景 -->
        <div class="auth-background">
            <div class="bg-shape bg-shape-1"></div>
            <div class="bg-shape bg-shape-2"></div>
            <div class="bg-shape bg-shape-3"></div>
        </div>
        <!-- 卡片 -->
        <div class="auth-card">
            <div class="auth-header">
                <div class="logo">
                    <div class="logo-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                            <path d="M2 17l10 5 10-5"/>
                            <path d="M2 12l10 5 10-5"/>
                        </svg>
                    </div>
                    <h1>CMS 管理</h1>
                </div>
                <p class="subtitle">{{ subtitle }}</p>
            </div>

            <!-- 表单区域由子页面通过插槽填充 -->
            <slot name="form"/>

            <!-- 页脚 -->
            <div class="auth-footer">
                <p>{{ footerText }}
                    <router-link :to="footerLink">{{ footerLinkText }}</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    subtitle: { type: String, default: '' },
    footerText: { type: String, default: '' },
    footerLink: { type: String, default: '/' },
    footerLinkText: { type: String, default: '' },
})
</script>

<style scoped>
/* ---- 容器 & 背景 ---- */
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    position: relative;
    overflow: hidden;
    padding: 20px;
}

.auth-background {
    position: absolute;
    inset: 0;
    overflow: hidden;
}

.bg-shape {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
}

.bg-shape-1 {
    width: 600px; height: 600px;
    background: linear-gradient(135deg, var(--primary-color, #667eea) 0%, #60CDFF 100%);
    top: -200px; right: -200px;
    animation: float 20s ease-in-out infinite;
}

.bg-shape-2 {
    width: 400px; height: 400px;
    background: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
    bottom: -100px; left: -100px;
    animation: float 15s ease-in-out infinite reverse;
}

.bg-shape-3 {
    width: 300px; height: 300px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    animation: pulse 10s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0); }
    50%      { transform: translate(30px, 30px); }
}

@keyframes pulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1);   opacity: 0.1; }
    50%      { transform: translate(-50%, -50%) scale(1.1); opacity: 0.15; }
}

/* ---- 卡片 ---- */
.auth-card {
    width: 100%;
    max-width: 420px;
    background: var(--card-bg);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
}

/* ---- 头部 / Logo ---- */
.auth-header {
    text-align: center;
    margin-bottom: 32px;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 12px;
}

.logo-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
}

.logo-icon svg { width: 28px; height: 28px; color: #fff; }

.logo h1 {
    margin: 0;
    font-size: 28px; font-weight: 700;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

/* ---- 表单通用样式（供子组件使用，不 scoped） ---- */
.auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.input-wrapper {
    display: flex;
    align-items: center;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.input-wrapper:focus-within {
    background: var(--bg-primary);
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px var(--primary-bg, rgba(64, 158, 255, 0.15));
}

.input-icon {
    width: 48px; height: 48px;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-tertiary);
    flex-shrink: 0;
}

.input-icon svg { width: 20px; height: 20px; }

.form-input {
    flex: 1;
    height: 48px;
    border: none;
    background: transparent;
    font-size: 15px;
    color: var(--text-primary);
    outline: none;
}

.form-input::placeholder { color: var(--text-tertiary); }

.input-suffix {
    width: 48px; height: 48px;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: color 0.3s ease;
    flex-shrink: 0;
}

.input-suffix:hover { color: var(--primary-color); }
.input-suffix svg { width: 20px; height: 20px; }

/* ---- 提交按钮 ---- */
.auth-btn {
    height: 50px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #60CDFF 100%);
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
    position: relative;
    overflow: hidden;
}

.auth-btn::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.6s ease;
}

.auth-btn:hover::before { left: 100%; }

.auth-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 120, 212, 0.5);
}

.auth-btn:active { transform: translateY(0); }

.auth-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
}

.loading-spinner {
    width: 20px; height: 20px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ---- 页脚 ---- */
.auth-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border-color);
}

.auth-footer p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

.auth-footer a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.auth-footer a:hover { color: var(--primary-hover); }

/* ---- el-form 深度覆盖 ---- */
:deep(.el-form-item) { margin-bottom: 0; }
:deep(.el-form-item__error) { padding-top: 4px; padding-left: 12px; }
</style>
