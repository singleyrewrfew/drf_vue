<template>
  <footer class="app-footer">
    <div class="footer-gradient"></div>
    <div class="footer-inner">
      <div class="footer-main">
        <div class="footer-brand">
          <div class="brand-content">
            <div class="footer-logo">
              <span class="logo-icon-small">Y</span>
              <span class="logo-text">YNCAQY</span>
            </div>
            <p class="brand-description">
              天底下没有什么所谓的无心之语，只有不小心说出的有心之言。
            </p>
          </div>
          <div class="ink-divider"></div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.app-footer {
  background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  color: var(--text-primary);
  margin-top: auto;
  position: relative;
  overflow: hidden;
}

.footer-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(45, 90, 74, 0.04) 0%, transparent 50%),
    radial-gradient(circle at 80% 30%, rgba(197, 61, 67, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.footer-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 40px 40px 24px;
  position: relative;
}

.footer-main {
  margin-bottom: 24px;
}

.footer-brand {
  margin-bottom: 16px;
}

.brand-content {
  max-width: 480px;
  margin: 0 auto;
  text-align: center;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.logo-icon-small {
  width: 36px;
  height: 36px;
  background: var(--vermilion-color);
  border-radius: var(--radius-xs);
  border: 2px solid var(--ink-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  font-family: 'SimSun', serif;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    2px 2px 8px rgba(197, 61, 67, 0.3);
  transition: transform var(--transition-normal);
}

.logo-icon-small:hover {
  transform: scale(1.05) rotate(-3deg);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.25),
    3px 3px 12px rgba(197, 61, 67, 0.4);
}

.logo-text {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: var(--tracking-wide);
  color: var(--text-primary);
  font-family: var(--font-display);
}

.brand-description {
  font-size: 15px;
  line-height: 2.0;
  color: var(--text-secondary);
  margin: 0;
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: var(--tracking-normal);
  position: relative;
  padding-left: 24px;
}

.brand-description::before {
  content: '"';
  position: absolute;
  left: 0;
  top: -4px;
  font-size: 28px;
  color: var(--vermilion-color);
  opacity: 0.5;
  font-family: Georgia, serif;
  line-height: 1;
}

/* 毛笔横线分隔符 */
.ink-divider {
  width: 60%;
  height: 2px;
  margin: 32px auto 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--text-tertiary) 20%,
    var(--text-secondary) 50%,
    var(--text-tertiary) 80%,
    transparent 100%
  );
  opacity: 0.6;
  position: relative;
}

.ink-divider::before,
.ink-divider::after {
  content: '✦';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  color: var(--primary-color);
  opacity: 0.8;
}

.ink-divider::before {
  left: -20px;
}

.ink-divider::after {
  right: -20px;
}

@media (max-width: 1024px) {
  .footer-inner {
    padding: 32px 24px 20px;
  }
}

@media (max-width: 768px) {
  .footer-inner {
    padding: 28px 20px 18px;
  }

  .footer-logo {
    margin-bottom: 10px;
  }

  .logo-text {
    font-size: 20px;
  }

  .brand-description {
    font-size: 13px;
    letter-spacing: 0.05em;
  }

  .ink-divider {
    width: 80%;
    margin-top: 24px;
  }
}

@media (max-width: 576px) {
  .footer-inner {
    padding: 24px 16px 16px;
  }

  .footer-logo {
    margin-bottom: 8px;
  }

  .logo-icon-small {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .logo-text {
    font-size: 18px;
  }

  .brand-description {
    font-size: 12px;
    padding-left: 20px;
  }

  .brand-description::before {
    font-size: 24px;
  }

  .ink-divider {
    width: 90%;
    margin-top: 20px;
  }
}
</style>
