from datetime import datetime

def parse_date_str(date_str: str, fmt: str = "%d/%m/%Y") -> datetime:
    return datetime.strptime(date_str, fmt)

def compare_dates(date1: str, date2: str, fmt: str = "%d/%m/%Y") -> bool:
    return parse_date_str(date1, fmt) == parse_date_str(date2, fmt) 