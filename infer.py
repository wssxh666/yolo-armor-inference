import cv2
import argparse
import os
import time  # <-- 新增：用于计时
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="YOLO 装甲板推理与关键点可视化")
    parser.add_argument('--model', type=str, default='weights/best.pt', help='模型权重路径')
    parser.add_argument('--source', type=str, default='videos/test.mp4', help='输入视频路径')
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
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args.output, fourcc, fps, (w, h))
    
    frame_count = 0
    total_objects = 0  # <-- 新增：用于统计检测到的总目标数
    
    print("[INFO] 开始推理...")
    
    # 预热一次模型，避免第一次推理的初始化耗时影响对比结果
    ret, frame = cap.read()
    if ret:
        model(frame, verbose=False)
        out.write(frame) # 保持输出视频完整
        frame_count += 1

    start_time = time.time()  # <-- 新增：开始计时

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        
        # 统计这一帧检测到的目标数量
        boxes = results[0].boxes
        if boxes is not None:
            total_objects += len(boxes)
            
        annotated_frame = results[0].plot()
        out.write(annotated_frame)
        frame_count += 1

    end_time = time.time()  # <-- 新增：结束计时
    total_time = end_time - start_time

    cap.release()
    out.release()
    
    print(f"[INFO] 推理完成！共处理 {frame_count} 帧，视频已保存至: {args.output}")
    print(f"==================================================")
    print(f"[RESULT] 总耗时: {total_time:.2f} 秒")
    print(f"[RESULT] 平均每帧耗时: {(total_time/frame_count)*1000:.2f} ms")
    print(f"[RESULT] 检测到的目标总数: {total_objects}")
    print(f"==================================================")

if __name__ == '__main__':
    main()