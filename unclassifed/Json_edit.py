import json

def json_to_dataframe(input_json):
    import pandas as pd
    # logger.info(f'Excute function >> json_to_dataframe')
    with open(input_json, "r", encoding='UTF-8') as f:
        try:
            jsonf = json.load(f)
            # logger.debug(f"Read complete!! >> {f} ")
        except:
            # logger.debug(f"Read Fail!! >> {f} ")
            print("errror 발생")
        key1 = list(jsonf.keys())[0] # 차트마다 달라짐
        # logger.debug(f"json chart종류 >> {key1} ")
        result = jsonf[key1]

        # DataFrame 만들기
        df_temp = pd.DataFrame(columns=result.keys())
        for key2 in result.keys():
            if result[key2] is None: #null값이 들어있는 경우
                df_temp[key2] = ""
            elif len(result[key2]) != 1:  # 데이터가 1개가 아닌 경우
                df_temp[key2] = [result[key2]]  # 한칸에 다 때려넣기
            else:
                df_temp[key2] = result[key2]
        df_temp["filename"] = [input_json]
    return df_temp