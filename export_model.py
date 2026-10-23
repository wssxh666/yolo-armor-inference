from ultralytics import YOLO

def export():
    # 1. 加载你之前用的模型
    model_path = "weights/best.pt"
    print(f"正在加载模型: {model_path}")
    model = YOLO(model_path)

    # 2. 导出为 ONNX 格式（通用格式，推荐）
    print("开始导出 ONNX 格式...")
    model.export(format="onnx")
    
    # 3. 导出为 TorchScript 格式（PyTorch 官方部署格式）
    print("开始导出 TorchScript 格式...")
    model.export(format="torchscript")

    print("两种格式导出完成！请查看 weights 文件夹。")

if __name__ == "__main__":
    export()