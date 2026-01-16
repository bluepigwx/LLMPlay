# 1. 先从 PyTorch 官方源安装 torch, torchvision, torchaudio
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# 2. 然后安装其他依赖（排除已安装的 torch 相关包）
pip install -r requirements.txt --no-deps
pip install -r requirements.txt

# 启动UI编辑器
pyqt6-tools designer