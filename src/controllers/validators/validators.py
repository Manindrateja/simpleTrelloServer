
from exception import CustomException

def validateRegister(data):
    if 'name' not in data:
        raise CustomException("please provice data")
    return True