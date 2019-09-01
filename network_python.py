import psutil
from time import sleep
import threading
import tkinter as tk
import tkinter.messagebox
import webbrowser
#软件版本控制的是exe文件版本，主要作用是软件功能上的：检查更新
from versions import network_version#軟件版本
import requests

network_list = [i for i in psutil.net_io_counters()]#获取网络数据
up_send = network_list[0]#发送数据包 单位字节
up_recv = network_list[1]#接受数据包 单位字节

def disponse_network():
    global up_send#本次发送速度结果
    global up_recv#本次接受速度结果

    sleep(1)#需要在采集这里等待一秒，正好一秒内速率（在其他地方延迟一秒都会导致速率不正确，测试过）

    network_list = [i for i in psutil.net_io_counters()]#获取网络数据
    network_send = network_list[0]#发送数据包 单位字节
    network_recv = network_list[1]#接受数据包 单位字节
    #现在的总数据字节减去上次的数据字节，等于现在的网速！
    temporary_send = network_send - up_send
    temporary_recv = network_recv - up_recv
    #判断是否大于1048576,则单位为mb,默认b
    if temporary_send >= 1048576:
        send_unit = "MB"
        send = (temporary_send // 1024) // 1024
    elif temporary_send >= 1024:# kb
        send_unit = "KB"
        send = temporary_send // 1024
    else:
        send = temporary_send
        send_unit = "B"

    if temporary_recv >= 1048576:# mb
        recv = (temporary_recv // 1024) //1024
        recv_unit = "MB"
    elif temporary_recv >= 1024:# kb
        recv_unit = "KB"
        recv = temporary_recv // 1024
    else:
        recv_unit = "B"
        recv = temporary_recv

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
    #添加標簽菜單
    #處理檢查更新
    def update_disponse():
        r = requests.get("https://raw.githubusercontent.com/qxkbwl/python_network_show/master/exe_versions.py")
        try:
            if r.text.split("=")[1] == network_version:
                tkinter.messagebox.showinfo(title='正在檢查更新', message='暫時沒有更新！') 
            else:
                webbrowser.open("https://github.com/qxkbwl/python_network_show/raw/master/dist/network_python.exe")
        except Exception:
            tkinter.messagebox.showinfo(title='檢查更新時出錯', message="报错内容：%s。請聯係管理員反饋"%(r.text))
            
    menuber = tk.Menu(windos) 
    update_menu = tk.Menu(menuber, tearoff=0)
    menuber.add_cascade(label="更多", menu=update_menu)
    # #加入小菜單
    update_menu.add_command(label="檢查更新", command=update_disponse)    
    

    windos.config(menu=menuber)
    windos.mainloop()


tk_th = threading.Thread(target=fun_tk, name="tk")

tk_th.start()

error_status = False
while True:
    # print(tk_th.is_alive())
    if not tk_th.is_alive() or error_status:
        break

    error_status = hit_me()
    
 
