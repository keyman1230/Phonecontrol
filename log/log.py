import logging

def set_log(module='log', path='Log',lv="INFO"):
    # 로그 생성
    logger = logging.getLogger(module) # 로거 모듈 수준 세팅

    # 로그의 출력 기준 설정
    logger.setLevel(getattr(logging, lv.upper()))

    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log 출력
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)

    # log를 파일에 출력
    file_handler = logging.FileHandler(f'{path}.log')
    file_handler.setFormatter(formatter) # 포매터 적용
    logger.addHandler(file_handler) # 핸들러 추가
    if module == "log":
        logger.info(f'Please confirm input parameter >> module')
    else:
        logger.info(f'Log Started')
    logger.info(f'Path >> {path}.log')
    logger.info(f'Setting Log Level >> {lv.upper()}')
    return logger


if __name__ == "__main__":
    set_log()