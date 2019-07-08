import psutil
from time import sleep
import threading
import tkinter as tk



network_list = [i for i in psutil.net_io_counters()]#获取网络数据
up_send = network_list[2]#发送数据包 单位字节
up_recv = network_list[3]#接受数据包 单位字节

def disponse_network():
    global up_send
    global up_recv

    network_list = [i for i in psutil.net_io_counters()]#获取网络数据
    network_send = network_list[2]#发送数据包 单位字节
    network_recv = network_list[3]#接受数据包 单位字节
    #现在的总数据字节减去上次的数据字节，等于现在的网速！
    network_send -= up_send
    network_recv -= up_recv
    #判断是否大于1048576,则单位为mb,默认kb
    if network_send >= 1048576:
        send_unit = "MB"
    elif network_recv >= 1025:# kb
        send_unit = "KB"
    else:
        send_unit = "b"

    if network_recv >= 1048576:# mb
        recv_unit = "MB"
    elif network_recv >= 1025:# kb
        recv_unit = "KB"
    else:
        recv_unit = "b"

    send = round(network_send/1024, 3)
    recv = round(network_recv/1024, 3)

    # print("发送：%s"%send)
    # print("接收：%s"%recv)
    sleep(1)
    # print('开始下一轮')
    #最后操作完成赋值这次的数据字节，下次再计算
    up_send = network_send
    up_recv = network_recv
    return send,send_unit, recv, recv_unit

def hit_me():
    send, send_unit, recv, recv_unit = disponse_network()
    try:
        var.set("发送：%s %s\n接收：%s %s"%(send, send_unit, recv, recv_unit))
        return False
    except:
        return True
    # print("发送：%s/n接收：%s"%(send, recv))
    

def fun_tk():
    windos = tk.Tk()

    windos.title("网速显示")

    windos.geometry("200x50")
    global var
    var = tk.StringVar()

    l = tk.Label(
        windos,
        textvariable=var,
        bg="green",
        font=("Arial",12),
        width=200,
        height=50,
    )
    l.pack()

    windos.mainloop()

tk_th = threading.Thread(target=fun_tk, name="tk")

tk_th.start()

error_status = False
while True:
    # print(tk_th.is_alive())
    if not tk_th.is_alive() or error_status:
        break

    error_status = hit_me()
        

