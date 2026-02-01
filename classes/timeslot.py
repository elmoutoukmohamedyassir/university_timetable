class TimeSlot:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
    
    def format_time(self, decimal_time):
        hours = int(decimal_time)
        minutes = int((decimal_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    def __str__(self):
        start_str = self.format_time(self.start_time)
        end_str = self.format_time(self.end_time)
        return f"[{self.day} | {start_str} - {end_str}]"