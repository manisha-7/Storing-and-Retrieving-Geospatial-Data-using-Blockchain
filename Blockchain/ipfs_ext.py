import Blockchain.ipfs 
import os
import time
import webbrowser
import shutil

def func():
    os.rename(f"media/{os.listdir('media')[0]}", 'media/abc.tif')
    # print(os.listdir('media')[0])
    os.system("python3 Blockchain/ipfs.py > Blockchain/mylog.txt")
    val = 'none'
    with open('Blockchain/mylog.txt','r') as file:
        c = 0
        # reading each line    
        for line in file:
            
            # reading each word        
            for word in line.split():
                c+=1
                if c==2:
                # displaying the words           
                    val = (word) 
                    # webbrowser.open(str('http://ipfs.io/ipfs/'+ word))
    shutil.rmtree('media')
    os.remove('Blockchain/mylog.txt')
    return val