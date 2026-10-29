import serial
import time
import struct

COM_PORT = 'COM5'         
BAUD_RATE = 115200        

def generate_rgb_packet(r, g, b, period_sec):
    """
    打包数据 (共 7 字节): [帧头1, 帧头2, R, G, B, Period, 校验位]
    """
    header1 = 0xAA
    header2 = 0x55
    # 将秒转换为 0.1 秒为单位 (比如 1.5 秒 -> 15)
    period_unit = int(period_sec * 10) & 0xFF 
    
    # 计算校验位
    checksum = (header1 + header2 + r + g + b + period_unit) & 0xFF
    
    # 使用 struct 打包成 7 个字节
    packet = struct.pack('<BBBBBBB', header1, header2, r, g, b, period_unit, checksum)
    return packet

def main():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print(f"✅ 串口已打开: {COM_PORT}，波特率: {BAUD_RATE}")
        
        while True:
            print("\n" + "="*30)
            # 1. 获取用户输入的颜色
            try:
                r = int(input("请输入红色值 R (0-255，直接回车默认255): ") or 255)
                g = int(input("请输入绿色值 G (0-255，直接回车默认0): ") or 0)
                b = int(input("请输入蓝色值 B (0-255，直接回车默认255): ") or 255)
                
                # 2. 获取用户输入的周期
                period_input = input("请输入呼吸周期 (秒，例如 2.5，直接回车默认2.0): ")
                period = float(period_input) if period_input else 2.0
                
                # 检查数值范围
                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                    print("❌ 错误：RGB 值必须在 0 到 255 之间！")
                    continue
                if period <= 0:
                    print("❌ 错误：周期必须大于 0！")
                    continue
                    
            except ValueError:
                print("❌ 错误：请输入有效的数字！")
                continue

            # 3. 打包并发送数据
            packet = generate_rgb_packet(r, g, b, period)
            print(f"\n发送数据: 颜色(RGB={r},{g},{b}), 周期={period}秒")
            print(f"原始十六进制字节流: {packet.hex().upper()}")
            
            ser.write(packet)
            print("✅ 数据发送完毕，请查看电控板子的灯！")
            
            # 询问是否继续测试
            cont = input("\n是否继续测试其他颜色/周期？(y/n, 默认 n): ")
            if cont.lower() != 'y':
                print("退出程序。")
                break
                
    except serial.SerialException as e:
        print(f"❌ 串口打开失败！请检查 COM 口是否正确，或者是否被串口助手占用。\n错误: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == '__main__':
    main()