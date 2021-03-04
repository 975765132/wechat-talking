import os

def imageDecode(dat_dir,dat_file_name):
    dat_read = open(dat_dir, "rb")
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    out=target_path+"\\"+dat_file_name+".jpg"
    png_write = open(out, "wb")
    for now in dat_read:
        for nowByte in now:
            newByte = nowByte ^ xor_value
            png_write.write(bytes([newByte]))
    dat_read.close()
    png_write.close()

def findFile(dat_path):
    fsinfo = os.listdir(dat_path)
    for dat_file_name in fsinfo:
        temp_path = os.path.join(dat_path, dat_file_name)
        if not os.path.isdir(temp_path):
            #print('文件路径: {}' .format(temp_path))
            imageDecode(temp_path,dat_file_name)
        else:
            pass
                        
if __name__=='__main__':

    # 修改.dat文件的存放路径
    dat_path = r'F:\WeChat Files\WeChat Files\wxid_v3z3560dy0j122\FileStorage\Image\2021-02'
    
    # 修改转换成png图片后的存放路径
    target_path = r'F:\WeChat Files\WeChat Files\wxid_v3z3560dy0j122\FileStorage\Image\Changed'
    
    # 修改加密的异或值,比如说我的异或值最后两位是B2，则xor_value = 0xB2，0x表示16进制
    xor_value = 0xE6
    
    findFile(dat_path)
    print("end")
