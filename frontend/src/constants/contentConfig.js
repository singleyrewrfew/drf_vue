export const CONTENT_STATUS_MAP = {
    draft: {label: '草稿', type: 'info'},
    published: {label: '已发布', type: 'success'},
    archived: {label: '已归档', type: 'warning'},
}

export const CONTENT_STATUS_OPTIONS = [
    {label: '草稿', value: 'draft'},
    {label: '已发布', value: 'published'},
    {label: '已归档', value: 'archived'},
]

export const ROLE_TYPE_MAP = {
    admin: 'danger',
    editor: 'warning',
    user: 'info',
}

export const BOOLEAN_OPTIONS = {
    true: {label: '是', type: 'success'},
    false: {label: '否', type: 'info'},
}

export const PERMISSION_OPTIONS = {
    true: {label: '允许', type: 'success'},
    false: {label: '禁止', type: 'info'},
}

export const ACTIVE_OPTIONS = {
    true: {label: '正常', type: 'success'},
    false: {label: '禁用', type: 'danger'},
}
