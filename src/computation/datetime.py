import datetime

def float_to_time(float_hour: float) -> str:
    # Chuyển đổi tổng số giờ thành đối tượng timedelta
    delta = datetime.timedelta(hours=float_hour)
    
    # Trả về chuỗi định dạng (str(delta) thường có dạng H:MM:SS)
    return str(delta)

if __name__ == "__main__":
    print(float_to_time(10.12)) # Output: 10:07:12