<template>
    <div class="auth-container">
        <!-- 背景层 -->
        <div class="auth-background">
            <div class="bg-grid"></div>
            <div class="bg-glow bg-glow-1"></div>
            <div class="bg-glow bg-glow-2"></div>
        </div>

        <!-- 卡片 -->
        <div class="auth-card">
            <div class="auth-header">
                <div class="logo">
                    <div class="logo-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                            <path d="M2 17l10 5 10-5"/>
                            <path d="M2 12l10 5 10-5"/>
                        </svg>
                    </div>
                    <h1>CMS 管理</h1>
                </div>
                <p class="subtitle">{{ subtitle }}</p>
            </div>

            <slot name="form"/>

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

<!-- ====== 布局样式（scoped）====== -->
<style scoped>
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    padding: 24px;

    /* 跟随主题的渐变背景 */
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%, var(--primary-bg) 0%, transparent 50%),
        radial-gradient(ellipse 60% 50% at 80% 100%, var(--primary-bg) 0%, transparent 50%),
        var(--bg-color);
}

/* ---- 背景层 ---- */
.auth-background {
    position: absolute;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
}

.bg-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(var(--border-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
    background-size: 48px 48px;
    opacity: 0.15;
    mask-image: radial-gradient(ellipse 70% 70% at center, black 30%, transparent 70%);
}

.bg-glow {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.4;
}

.bg-glow-1 {
    width: 500px; height: 500px;
    background: var(--primary-color);
    opacity: 0.08;
    top: -180px; right: -120px;
    animation: glow-drift-1 18s ease-in-out infinite;
}

.bg-glow-2 {
    width: 400px; height: 400px;
    background: var(--primary-light, #60A5FA);
    opacity: 0.06;
    bottom: -120px; left: -100px;
    animation: glow-drift-2 22s ease-in-out infinite reverse;
}

@keyframes glow-drift-1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%      { transform: translate(-25px, 20px) scale(1.05); }
    66%      { transform: translate(15px, -15px) scale(0.97); }
}

@keyframes glow-drift-2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%      { transform: translate(20px, -18px) scale(1.04); }
    66%      { transform: translate(-12px, 12px) scale(0.96); }
}

/* ---- 卡片 ---- */
.auth-card {
    width: 100%;
    max-width: 400px;
    background: var(--card-bg, #FFFFFF);
    border-radius: var(--radius-lg, 12px);
    padding: 28px 26px 20px;
    position: relative;
    z-index: 1;
    max-height: calc(100vh - 48px);
    overflow-y: auto;
    overscroll-behavior: contain;

    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow:
        var(--shadow-xl, 0 16px 48px rgba(0, 0, 0, 0.16)),
        0 0 80px -20px var(--primary-bg);

    border: 1px solid var(--border-light, #F0F0F0);
}

/* ---- 头部 / Logo ---- */
.auth-header {
    text-align: center;
    margin-bottom: 18px;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 8px;
}

.logo-icon {
    width: 38px; height: 38px;
    display: flex; align-items: center; justify-content: center;
    border-radius: var(--radius-md, 8px);
    background: var(--primary-color, #0078D4);
    box-shadow:
        0 4px 14px -3px rgba(0, 120, 212, 0.35),
        inset 0 1px 0 rgba(255,255,255,0.15);
    position: relative;
    overflow: hidden;
}

.logo-icon::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(to bottom, rgba(255,255,255,0.18), transparent);
    border-radius: var(--radius-md, 8px) var(--radius-md, 8px) 0 0;
}

.logo-icon svg {
    width: 22px; height: 22px;
    color: #fff;
    position: relative;
    z-index: 1;
}

.logo h1 {
    margin: 0;
    font-size: 22px; font-weight: 700;
    letter-spacing: -0.2px;
    color: var(--text-primary, #1A1A1A);
}

.subtitle {
    margin: 0;
    color: var(--text-secondary, #616161);
    font-size: 14px;
    font-weight: 400;
    line-height: 1.5;
}

/* ---- 页脚 ---- */
.auth-footer {
    text-align: center;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--border-light, #F0F0F0);
}

.auth-footer p {
    margin: 0;
    color: var(--text-secondary, #616161);
    font-size: 13px;
}

.auth-footer a {
    color: var(--primary-color, #0078D4);
    text-decoration: none;
    font-weight: 600;
    transition: color 0.25s ease;
}
.auth-footer a:hover { color: var(--primary-hover, #106EBE); }

/* ---- 响应式 ---- */
@media (max-width: 480px) {
    .auth-container { padding: 12px; }
    .auth-card {
        padding: 22px 18px 16px;
        max-height: calc(100vh - 24px);
    }
    .logo h1 { font-size: 20px; }
    .auth-header { margin-bottom: 14px; }
    .auth-footer { margin-top: 12px; padding-top: 12px; }
}
</style>

<!-- ====== 表单 / 按钮样式（非 scoped，穿透插槽） ====== -->
<style>
/* ---- 表单容器 ---- */
.auth-form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.form-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary, #616161);
    letter-spacing: 0.2px;
    text-transform: uppercase;
}

/* ---- el-form 覆盖 ---- */
.auth-form .el-form-item { margin-bottom: 0; }
.auth-form .el-form-item__error {
    padding-top: 3px;
    padding-left: 2px;
    font-size: 11px;
    color: var(--danger-color, #D13438);
}
</style>
