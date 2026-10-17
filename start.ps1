$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    # 已打开的编辑器可能没有继承后来保存的用户模型配置。
    foreach ($name in @('API_KEY', 'BASE_URL', 'MODEL', 'LLM_API_KEY', 'LLM_PROVIDER', 'LLM_MODEL', 'LLM_BASE_URL', 'SILICONFLOW_API_KEY', 'SILICONFLOW_BASE_URL', 'SILICONFLOW_MODEL', 'DEEPSEEK_API_KEY')) {
        if (-not [Environment]::GetEnvironmentVariable($name, 'Process')) {
            $value = [Environment]::GetEnvironmentVariable($name, 'User')
            if ($value) { [Environment]::SetEnvironmentVariable($name, $value, 'Process') }
        }
    }
    docker compose -f docker/docker-compose.yaml up -d mysql elasticsearch qdrant embedding
    if ($LASTEXITCODE -ne 0) { throw '基础服务启动失败，请检查 Docker Desktop。' }
    & ./.venv/Scripts/python.exe main.py
    if ($LASTEXITCODE -ne 0) { throw '应用启动失败，请检查上方错误。' }
}
finally {
    Pop-Location
}
