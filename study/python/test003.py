log_data = { "file_gbn" : ["W01","W02","A01"] , "file_path" : ["C:/workSpace/Urllog/WEB01","C:/workSpace/Urllog/WEB02","C:/workSpace/Urllog/WAS01"]}

if __name__ == '__main__':
    idx = 0
    for log_gbn in log_data['file_gbn']:
        log_path = log_data['file_path'][idx]
        print("idx={0} --- {1} : {2} ".format(idx,log_gbn,log_path))
        idx = idx + 1
