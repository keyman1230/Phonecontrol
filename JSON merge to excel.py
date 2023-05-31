from log import log
from file_control import untitled as ut
from unclassifed import time, Json_edit




if __name__ == "__main__":
    logger = log.set_log(module="Json_Merge", path=f"Json_Merge", lv="INFO") # 로깅 설정
    # logger.info("test logging")
    target_dir = ut.select_folder_location(init_dir="D:\# Shared_Folder_HDD\# Image Database\# Resolution\# 2023\23-05-30 Huawei BM\DOF\Best Focus Find\P60 Pro\Results") #  Json이 위치한 폴더
    target_filelist = ut.make_filelist(target_dir=target_dir, subdir=False, list_filetype=['.json']) # Json 목록
    t = time.return_now() # 현재시간 stfrtime 형식으로 가져오기

    save_file_name = f"{target_dir}//Result_{t}.xlsx"

    ###### 1-1. Excel save format 지정 #######
    import pandas as pd
    writer = pd.ExcelWriter(save_file_name, engine='xlsxwriter')
    # logger.debug(f"excel file path = {excelfilepath}")

    ##### 3-1 단순 합치기
    ###### 3. Converting json and export to excel
    import pandas as pd
    SummaryDF = pd.DataFrame()
    for jsonfile in target_filelist:
        sampleDF = Json_edit.json_to_dataframe(jsonfile)
        logger.debug(f"sample dataframe shape = {sampleDF.shape}")
        SummaryDF = pd.concat([SummaryDF, sampleDF], axis=0)
    SummaryDF.to_excel(excel_writer=writer, sheet_name="DeadLeaves")
    writer.save()
    # logger.debug(f"Merge complete!! ")
