# yolo-armor-inference

## 1. 项目完成的功能
本项目基于 YOLO26n 装甲板模型（`best.pt`），编写了 Python 推理脚本 `infer.py`。具体功能包括：
*   加载模型权重，读取自己拍摄的视频文件。
*   对视频逐帧执行推理。
*   在检测到目标时，显示检测框、类别、置信度，以及该目标的 4 个关键点。
*   保存与原视频内容对应、能够正常播放的推理结果视频。

## 2. 运行环境与硬件
*   **Python版本**：Python 3.12.x
*   **主要依赖**：`ultralytics`、`opencv-python`（具体版本见 `requirements.txt`）。
*   **硬件**：本次作业使用 **CPU** 运行（若环境有 NVIDIA 显卡并安装 CUDA，代码会自动切换为 GPU）。

## 3. 模型权重的准备与放置
*   **准备方式**：模型权重 `best.pt` 需从课程参考材料中获取。
*   **放置位置**：请在项目根目录下新建 `weights` 文件夹，将 `best.pt` 放置在 `weights/` 目录下，即 `weights/best.pt`。
*   *注：模型权重文件较大，未提交至 Git 历史中，需按上述方式自行准备。*

## 4. 依赖安装、运行命令与结果说明
**依赖安装步骤：**
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

**实际运行命令：**
```bash
# 默认使用默认路径
py -3.12 infer.py

# 或者通过命令行参数指定路径（模型路径、视频路径、输出位置均可自定义）
py -3.12 infer.py --model weights/best.pt --source videos/test.mp4 --output output/result.avi
