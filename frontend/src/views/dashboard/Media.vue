<template>
    <div class="media-page">
        <!--
            TablePage: 通用表格页面组件
            - :show-create="false / :show-edit="false 隐藏新建/编辑按钮（媒体通过上传创建）
            - v-model:page / v-model:page-size 双向绑定分页
            - #header 自定义头部插槽：替换默认的"新建"按钮为"上传"按钮
            - #row-actions 自定义操作插槽：预览和复制链接
        -->
        <TablePage
            ref="tableRef"
            title="媒体管理"
            :show-create="false"
            :show-edit="false"
            :data="mediaList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :actions-width="280"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!-- 自定义卡片头部：标题 + 上传按钮 -->
            <template #header>
                <div class="card-header">
                    <span>媒体管理</span>
                    <!-- 文件上传组件 -->
                    <el-upload
                        :action="uploadUrl"
                        :headers="uploadHeaders"
                        :before-upload="validateFile"
                        :on-success="onUploadSuccess"
                        :on-error="handleUploadError"
                        :on-progress="handleUploadProgress"
                        :on-change="handleFileChange"
                        :show-file-list="false"
                        multiple
                    >
                        <UploadButton
                            :loading="uploading"
                            :progress="uploadProgress"
                            :text="uploadButtonText"
                        />
                    </el-upload>
                </div>
            </template>

            <!-- 文件名：支持超长文件名省略显示 -->
            <el-table-column prop="filename" label="文件名" min-width="200" show-overflow-tooltip/>
            <!-- MIME 类型（如 image/jpeg、video/mp4） -->
            <el-table-column prop="file_type" label="类型" width="150"/>
            <!-- 文件大小：自动格式化为 B/KB/MB -->
            <el-table-column prop="file_size" label="大小" width="100">
                <template #default="{ row }">
                    {{ formatSize(row.file_size) }}
                </template>
            </el-table-column>
            <!-- 缩略图状态：仅视频文件有缩略图生成任务 -->
            <el-table-column label="缩略图" width="150">
                <template #default="{ row }">
                    <ThumbnailStatus
                        v-if="row.is_video"
                        :status="row.thumbnail_status"
                        @retry="handleRegenerateThumbnails(row)"
                    />
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <!-- 上传者名称 -->
            <el-table-column prop="uploader_name" label="上传者" width="120"/>
            <!-- 上传时间 -->
            <el-table-column prop="created_at" label="上传时间" width="180"/>
            <!-- 文件存储路径 -->
            <el-table-column prop="url" label="文件路径" width="180" show-overflow-tooltip/>

            <!-- 自定义操作列：预览 + 复制链接 -->
            <!-- 注意：TablePage 的操作列插槽名为 row-actions（非 actions），
                 此插槽内容会追加到内置编辑/删除按钮之前 -->
            <template #row-actions="{ row }">
                <!-- 打开预览弹窗 -->
                <ActionButton icon="preview" text="预览" type="info" @click="openPreview(row)"/>
                <!-- 复制文件 URL 到剪贴板 -->
                <ActionButton icon="copy" text="链接" @click="copyLink(row)"/>
            </template>
        </TablePage>

        <!--
            媒体预览弹窗
            根据文件类型展示不同的预览方式：
              - 图片：直接显示图片
              - 视频：使用 VideoPlayer 组件播放
              - 音频：使用原生 audio 标签
              - 其他：提示不支持预览，提供下载按钮
        -->
        <el-dialog
            v-model="previewVisible"
            :title="previewFile?.filename || '预览'"
            :width="dialogWidth"
            destroy-on-close
        >
            <div class="preview-container">
                <!-- 图片预览 -->
                <img v-if="isImage" :src="previewUrl" class="preview-image" alt="预览图片"/>
                <!-- 视频预览（含缩略图导航） -->
                <VideoPlayer
                    v-else-if="isVideo"
                    :key="previewFile?.id"
                    :src="previewUrl"
                    :poster="videoPoster"
                    :thumbnails="videoThumbnails"
                    :thumbnails-count="videoThumbnailsCount"
                    @error="onVideoError"
                />
                <!-- 音频预览 -->
                <audio v-else-if="isAudio" :src="previewUrl" controls class="preview-audio"/>
                <!-- 不支持的文件类型 -->
                <div v-else class="preview-unsupported">
                    <el-icon :size="64"><Document/></el-icon>
                    <p>该文件类型不支持预览</p>
                    <el-button type="primary" @click="downloadFile">下载文件</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
/**
 * @file 媒体管理页面 (Media Index)
 * @description 管理系统中的媒体文件（上传、预览、删除、缩略图管理）。
 *              这是一个功能丰富的页面，整合了多个专用 Composables。
 *
 * 页面功能：
 *   1. 展示媒体文件列表（分页表格）
 *   2. 上传新文件（自定义 header 插槽中的上传按钮）
 *   3. 预览文件（弹窗，支持图片/视频/音频）
 *   4. 删除文件（二次确认后执行）
 *   5. 视频缩略图管理（SSE 实时更新缩略图生成进度）
 *   6. 复制文件链接到剪贴板
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑
 *   - useDelete: 处理删除操作
 *   - useMediaUpload: 封装文件上传流程（验证、进度、成功/失败处理）
 *   - useMediaPreview: 封装文件预览流程（类型判断、URL构建、弹窗控制）
 *   - useThumbnailSSE: 封装 Server-Sent Events 连接（视频缩略图实时状态推送）
 *
 * @requires vue - Vue 3 核心库
 * @requires element-plus - UI 组件库
 * @requires @element-plus/icons-vue - Element Plus 图标库
 * @requires @/api/media - 媒体相关的 API 接口
 * @requires @/composables - 专用 Composables（上传/预览/SSE）
 * @requires @/composables/usePagination - 分页组合式函数
 * @requires @/composables/useFormSubmit - 删除组合式函数
 * @requires @/components/TablePage.vue - 通用表格页面组件
 * @requires @/components/VideoPlayer.vue - 视频播放器组件
 * @requires @/components/PreviewButton.vue - 预览按钮组件
 * @requires @/components/UploadButton.vue - 上传按钮组件
 * @requires @/components/ThumbnailStatus.vue - 缩略图状态组件
 */

// ============================================================================
// 【1】依赖导入
// ============================================================================

/** Vue 响应式 API */
import {watch, onMounted, onUnmounted} from 'vue'

/** Element Plus */
import {ElMessage} from 'element-plus'
import {Document} from '@element-plus/icons-vue'

/**
 * API 接口
 * - getMedia: 获取媒体文件列表（支持分页）
 * - deleteMedia: 删除指定媒体文件
 * - regenerateThumbnails: 重新生成视频缩略图
 */
import {getMedia, deleteMedia, regenerateThumbnails} from '@/api/media'

/** 业务组件 */
import VideoPlayer from '@/components/VideoPlayer.vue'
import TablePage from '@/components/TablePage.vue'
import ActionButton from '@/components/ActionButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import ThumbnailStatus from '@/components/ThumbnailStatus.vue'

/** 通用 Composables */
import {usePagination} from '@/composables/usePagination'
import {useDelete} from '@/composables/useFormSubmit'

/** 媒体专用 Composables */
import {
    useMediaUpload,
    useMediaPreview,
    useThumbnailSSE,
} from '@/composables'


// ============================================================================
// 【2】Composables 初始化
// ============================================================================

/** API 基础地址（用于构建上传 URL 和预览 URL） */
const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * 分页列表管理实例
 *
 * @type {Object}
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     *
     * @param {Object} params - 分页参数 {limit, offset}
     * @returns {Promise<Object>} DRF 格式的响应数据
     */
    async (params) => {
        const {data} = await getMedia(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref
// ============================================================================

/** @type {Ref<Array>} 媒体文件列表 */
const mediaList = pagination.data

/** @type {Ref<boolean>} 加载状态 */
const loading = pagination.loading

/** @type {Ref<number>} 当前页码 */
const page = pagination.page

/** @type {Ref<number>} 每页显示条数 */
const pageSize = pagination.pageSize

/** @type {Ref<number>} 总记录数 */
const total = pagination.total

/**
 * 刷新数据的快捷方法
 * @returns {Promise<void>}
 */
const refreshData = () => pagination.fetchData()

/**
 * 删除操作管理实例
 *
 * @type {Object}
 */
const delOp = useDelete(
    (id) => deleteMedia(id),
    {message: '确定删除该文件？'}
)

// ============================================================================
// 【2.2】媒体专用 Composables 初始化
// ============================================================================

/**
 * 文件上传相关状态和方法
 *
 * 由 useMediaUpload 提供，封装了：
 *   - 上传 URL 和认证头
 *   - 文件类型/大小校验
 *   - 上传进度追踪
 *   - 成功/错误回调处理
 */
const {
    /** @type {Ref<boolean>} 是否正在上传 */
    uploading,
    /** @type {Ref<number>} 上传进度百分比（0-100） */
    uploadProgress,
    /** @type {string} 上传接口 URL */
    uploadUrl,
    /** @type {Object} 上传请求头（包含认证 Token） */
    uploadHeaders,
    /** @type {Ref<string>} 上传按钮文字（随状态变化） */
    uploadButtonText,
    /** @type {Function} 文件上传前校验 */
    validateFile,
    /** @type {Function} 文件选择变化回调 */
    handleFileChange,
    /** @type {Function} 上传进度变化回调 */
    handleUploadProgress,
    /**
     * 上传成功回调
     * 签名: handleUploadSuccess(response, file, fileList, callbacks?)
     * callbacks.onSuccess(mediaData) — 单文件成功时触发
     * @type {Function}
     */
    handleUploadSuccess,
    /** @type {Function} 上传失败回调 */
    handleUploadError,
} = useMediaUpload(baseUrl)

/**
 * 媒体预览相关状态和方法
 *
 * 由 useMediaPreview 提供，封装了：
 *   - 预览弹窗开关控制
 *   - 文件类型自动识别（图片/视频/音频/其他）
 *   - 预览 URL 构建
 *   - 视频缩略图信息
 *   - 复制链接/下载功能
 */
const {
    /** @type {Ref<boolean>} 预览弹窗是否可见 */
    previewVisible,
    /** @type {Ref<Object|null>} 正在预览的文件对象 */
    previewFile,
    /** @type {Ref<string|null>} 视频封面图 URL */
    videoPoster,
    /** @type {Ref<boolean>} 是否为图片类型 */
    isImage,
    /** @type {Ref<boolean>} 是否为视频类型 */
    isVideo,
    /** @type {Ref<boolean>} 是否为音频类型 */
    isAudio,
    /** @type {Ref<string>} 预览 URL（完整可访问路径） */
    previewUrl,
    /** @type {Ref<Array>} 视频缩略图数组 */
    videoThumbnails,
    /** @type {Ref<number>} 视频缩略图总数 */
    videoThumbnailsCount,
    /** @type {ComputedRef<string|number>} 弹窗宽度（根据文件类型自适应） */
    dialogWidth,
    /** @type {Function} 打开预览弹窗 */
    openPreview,
    /** @type {Function} 复制文件链接 */
    copyLink,
    /** @type {Function} 下载文件 */
    downloadFile,
    /** @type {Function} 视频播放出错回调 */
    onVideoError,
} = useMediaPreview(baseUrl)

/**
 * 视频缩略图 SSE 相关方法
 *
 * 由 useThumbnailSSE 提供，用于通过 Server-Sent Events 实时接收
 * 视频文件缩略图生成的进度通知。
 */
const {
    /** @type {Function} 订阅指定视频的缩略图状态变更 */
    subscribeToThumbnailStatus,
    /** @type {Function} 关闭所有 SSE 连接（组件卸载时清理） */
    closeAllConnections,
} = useThumbnailSSE(baseUrl)


// ============================================================================
// 【3】工具函数与事件处理
// ============================================================================

/**
 * 格式化文件大小为人类可读字符串
 *
 * @param {number} bytes - 文件字节数
 * @returns {string} 格式化后的字符串（如 "1.5 MB"、"256 KB"）
 */
const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

/**
 * SSE 数据更新回调 — 更新媒体列表中对应记录的缩略图状态
 *
 * 当服务端通过 SSE 推送缩略图生成进度时调用，
 * 实时更新表格中对应行的缩略图状态。
 *
 * @param {Object} sseData - SSE 推送的数据
 * @param {number} sseData.media_id - 对应的媒体文件 ID
 * @param {string} sseData.thumbnail_status - 新的缩略图状态
 * @param {string} [sseData.thumbnails_url] - 缩略图 URL
 * @param {number} [sseData.thumbnails_count] - 缩略图数量
 */
const updateMediaFromSSE = (sseData) => {
    const mediaId = sseData.media_id
    const index = mediaList.value.findIndex(m => m.id === mediaId)
    if (index === -1) return  // 未在当前页找到对应记录，忽略

    // 更新该条记录的缩略图相关信息
    mediaList.value[index].thumbnail_status = sseData.thumbnail_status
    if (sseData.thumbnails_url) {
        mediaList.value[index].thumbnails_url = sseData.thumbnails_url
    }
    if (sseData.thumbnails_count) {
        mediaList.value[index].thumbnails_count = sseData.thumbnails_count
    }
}

/**
 * SSE 回调配置对象
 *
 * 将状态变更和完成事件统一指向 updateMediaFromSSE 处理函数。
 *
 * @type {Object}
 * @property {Function} onStatusChange - 状态变更时的回调
 * @property {Function} onComplete - 生成完成时的回调
 */
const sseCallbacks = {
    onStatusChange: updateMediaFromSSE,
    onComplete: updateMediaFromSSE,
}

/**
 * 文件上传成功后的增强回调
 *
 * 通过 handleUploadSuccess 的 callbacks.onSuccess 钩子，
 * 在基础上传逻辑（进度更新、成功提示、状态重置）之上追加：
 *   1. 视频文件 → 订阅缩略图 SSE 状态
 *   2. 新文件插入列表顶部（无需全量刷新）
 *
 * @param {Object} mediaData - 上传接口返回的媒体数据
 */
const onMediaUploaded = (mediaData) => {
    // 视频文件 → 订阅缩略图 SSE
    if (mediaData?.is_video && mediaData?.id) {
        subscribeToThumbnailStatus(mediaData.id, sseCallbacks)
    }

    // 将新文件插入列表顶部（避免全量刷新）
    if (mediaData?.id) {
        const exists = mediaList.value.some(m => m.id === mediaData.id)
        if (!exists) {
            mediaList.value.unshift(mediaData)
            total.value += 1
        }
    }
}

/**
 * 上传成功处理函数（传递给 el-upload :on-success）
 *
 * 调用 composable 提供的 handleUploadSuccess，并注入增强回调。
 */
const onUploadSuccess = (response, file, fileList) => {
    handleUploadSuccess(response, file, fileList, {
        onSuccess: onMediaUploaded,
    })
}

/**
 * 重新生成视频缩略图
 *
 * 用于当视频缩略图生成失败时手动触发重新生成。
 *
 * @async
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 媒体文件 ID
 * @returns {Promise<void>}
 */
const handleRegenerateThumbnails = async (row) => {
    try {
        await regenerateThumbnails(row.id)
        ElMessage.success('缩略图生成任务已启动')
        // 刷新列表以更新缩略图状态
        await refreshData()
    } catch {
        ElMessage.error('启动缩略图生成失败')
    }
}


// ============================================================================
// 【4】分页变化监听
// ============================================================================

/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 *
 * 合并监听避免切换 pageSize 时产生双重 API 请求。
 */
watch([page, pageSize], () => {
    refreshData()
})


// ============================================================================
// 【5】生命周期
// ============================================================================

/**
 * 组件挂载后加载第一页媒体数据
 */
onMounted(() => {
    refreshData()
})

/**
 * 组件卸载时关闭所有 SSE 连接
 * 防止内存泄漏和无效的网络请求。
 */
onUnmounted(() => {
    closeAllConnections()
})
</script>

<style scoped>
/**
 * 媒体管理页面样式
 */
.media-page {
    padding: 20px;
}

/** 卡片头部布局（标题 + 上传按钮左右分布） */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/** 预览容器（居中对齐） */
.preview-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}

/** 图片预览（限制最大尺寸以适应弹窗） */
.preview-image {
    max-width: 100%;
    max-height: 60vh;
    object-fit: contain;
}

/** 音频预览（撑满宽度） */
.preview-audio {
    width: 100%;
}

/** 不支持的文件类型提示 */
.preview-unsupported {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    color: #909399;
}

.preview-unsupported p {
    margin: 0;
}
</style>
