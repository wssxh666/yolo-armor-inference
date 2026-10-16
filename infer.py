import cv2
import argparse
import os
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="YOLO 装甲板推理与关键点可视化")
    parser.add_argument('--model', type=str, default='weights/best.pt', help='模型权重路径')
    parser.add_argument('--source', type=str, default='videos/test.mp4', help='输入视频路径')
    # 注意这里改成了 .avi 后缀，避免 Windows 下 MP4 编码失败
    parser.add_argument('--output', type=str, default='output/result.avi', help='输出视频保存路径')
    return parser.parse_args()

def main():
    args = parse_args()
    
    print(f"[INFO] 正在加载模型: {args.model}")
    model = YOLO(args.model)
    
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"[ERROR] 无法打开视频: {args.source}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 确保输出文件夹存在
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # 使用 XVID 编码器，生成 .avi 文件，保证在 Windows 下能正常播放
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args.output, fourcc, fps, (w, h))
    
    print(f"[INFO] 开始推理，输出保存至: {args.output}")

    # 逐帧推理
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 执行推理
        results = model(frame, verbose=False)
        
        # 绘制检测框、类别、置信度和 4 个关键点
        annotated_frame = results[0].plot()
        
        # 写入保存
        out.write(annotated_frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"[INFO] 已处理 {frame_count} 帧...")

    cap.release()
    out.release()
    print(f"[INFO] 推理完成！共处理 {frame_count} 帧，视频已保存！")

if __name__ == '__main__':
    main()