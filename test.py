import base64

with open("F:\\WeChat Files\\WeChat Files\\wxid_v3z3560dy0j122\\FileStorage\\Image\\2021-02\\4cb55414294bd496f7da0af6be62e5fe.dat", "rb") as rf:  # 读取图片
    base64_data = base64.b64encode(rf.read())  # 转化为base64
    ImageBase64 = base64_data.decode()