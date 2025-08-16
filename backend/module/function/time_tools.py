from datetime import datetime, timedelta
import calendar
import re
from dateutil.relativedelta import relativedelta

class TimeCalculator:
    """
    Enhanced utility class for complex time and date calculations
    Provides methods to calculate dates based on various time references
    """
    
    def __init__(self):
        """Initialize with current date"""
        self.current_date = datetime.now()
    
    def get_current_date(self):
        """Get current date in formatted string"""
        return self.current_date.strftime("%Y-%m-%d")
    
    def get_current_weekday(self):
        """Get current weekday in Vietnamese"""
        weekdays = {
            0: "Thứ 2",
            1: "Thứ 3", 
            2: "Thứ 4",
            3: "Thứ 5",
            4: "Thứ 6",
            5: "Thứ 7",
            6: "Chủ nhật"
        }
        return weekdays[self.current_date.weekday()]
    
    def parse_complex_time_reference(self, text):
        """
        Parse complex Vietnamese time references and convert to target date
        
        Args:
            text (str): Text containing complex time reference
            
        Returns:
            dict: Date information including calculated date and metadata
        """
        text = text.lower().strip()
        
        # Handle "thứ X tuần sau" pattern
        weekday_pattern = r"thứ\s*(\d+)\s*tuần\s*sau"
        weekday_match = re.search(weekday_pattern, text)
        if weekday_match:
            return self._calculate_next_weekday(int(weekday_match.group(1)))
        
        # Handle "chủ nhật tuần sau" pattern
        if "chủ nhật tuần sau" in text:
            # Map Chủ nhật to internal number 8 to produce python weekday 6
            return self._calculate_next_weekday(8)
        
        # Handle "thứ X tuần trước" pattern
        weekday_prev_pattern = r"thứ\s*(\d+)\s*tuần\s*trước"
        weekday_prev_match = re.search(weekday_prev_pattern, text)
        if weekday_prev_match:
            return self._calculate_previous_weekday(int(weekday_prev_match.group(1)))
        
        # Handle "chủ nhật tuần trước" pattern
        if "chủ nhật tuần trước" in text:
            # Map Chủ nhật to internal number 8 to produce python weekday 6
            return self._calculate_previous_weekday(8)
        
        # Handle "ngày này tháng sau" pattern
        if "ngày này tháng sau" in text:
            return self._calculate_same_day_next_month()
        
        # Handle "ngày này tháng trước" pattern
        if "ngày này tháng trước" in text:
            return self._calculate_same_day_previous_month()
        
        # Handle "ngày này năm sau" pattern
        if "ngày này năm sau" in text:
            return self._calculate_same_day_next_year()
        
        # Handle "ngày này năm trước" pattern
        if "ngày này năm trước" in text:
            return self._calculate_same_day_previous_year()
        
        # Handle "X năm nữa" pattern
        years_pattern = r"(\d+)\s*năm\s*nữa"
        years_match = re.search(years_pattern, text)
        if years_match:
            return self._calculate_years_ahead(int(years_match.group(1)))
        
        # Handle "X tháng nữa" pattern
        months_pattern = r"(\d+)\s*tháng\s*nữa"
        months_match = re.search(months_pattern, text)
        if months_match:
            return self._calculate_months_ahead(int(months_match.group(1)))
        
        # Handle "X tuần nữa" pattern
        weeks_pattern = r"(\d+)\s*tuần\s*nữa"
        weeks_match = re.search(weeks_pattern, text)
        if weeks_match:
            return self._calculate_weeks_ahead(int(weeks_match.group(1)))
        
        # Handle simple Vietnamese time references first (exact matches)
        simple_mapping = {
            "hôm nay": 0,
            "ngày mai": 1,
            "ngày mốt": 1,  # Thêm "ngày mốt" = "ngày mai"
            "ngày kia": 2,
        }
        
        for reference, days in simple_mapping.items():
            if reference in text:
                return self._calculate_days_ahead(days)
        
        # Handle "X ngày nữa" pattern (more flexible)
        days_pattern = r"(\d+)\s*ngày\s*nữa"
        days_match = re.search(days_pattern, text)
        if days_match:
            return self._calculate_days_ahead(int(days_match.group(1)))
        
        # Handle "X tuần nữa" pattern
        weeks_pattern = r"(\d+)\s*tuần\s*nữa"
        weeks_match = re.search(weeks_pattern, text)
        if weeks_match:
            return self._calculate_weeks_ahead(int(weeks_match.group(1)))
        
        # Handle "X tháng nữa" pattern
        months_pattern = r"(\d+)\s*tháng\s*nữa"
        months_match = re.search(months_pattern, text)
        if months_match:
            return self._calculate_months_ahead(int(months_match.group(1)))
        
        # Handle "cuối tháng" pattern
        if "cuối tháng" in text:
            return self._calculate_end_of_month()
        
        # Handle "đầu tháng" pattern
        if "đầu tháng" in text:
            return self._calculate_start_of_month()
        
        # Handle "cuối tuần" pattern
        if "cuối tuần" in text:
            return self._calculate_end_of_week()
        
        # Handle "đầu tuần" pattern
        if "đầu tuần" in text:
            return self._calculate_start_of_week()
        
        # Default to today if no match found
        return self._calculate_days_ahead(0)
    
    def _calculate_next_weekday(self, target_weekday):
        """
        Calculate specific weekday in next week (next week, not current week)
        
        Args:
            target_weekday (int): Target weekday (1-7, where 1 is Monday)
            
        Returns:
            dict: Date information for target weekday
        """
        # Convert Vietnamese weekday number to Python weekday (0-6, where 0 is Monday)
        python_weekday = self._convert_thu_to_python_weekday(target_weekday)
        
        # Find Monday of current week
        monday_this_week = self.current_date - timedelta(days=self.current_date.weekday())
        # Add 7 days to get Monday of next week
        monday_next_week = monday_this_week + timedelta(days=7)
        # Add the target weekday offset (0=Monday, 1=Tuesday, etc.)
        target_date = monday_next_week + timedelta(days=python_weekday)
        
        days_ahead = (target_date - self.current_date).days
        
        return {
            "time_reference": f"thứ {target_weekday} tuần sau",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_ahead,
            "calculation_type": "next_weekday"
        }
    
    def _calculate_previous_weekday(self, target_weekday):
        """
        Calculate specific weekday in previous week (previous week, not current week)
        
        Args:
            target_weekday (int): Target weekday (1-7, where 1 is Monday)
            
        Returns:
            dict: Date information for target weekday
        """
        # Convert Vietnamese weekday number to Python weekday (0-6, where 0 is Monday)
        python_weekday = self._convert_thu_to_python_weekday(target_weekday)

        # Find the previous occurrence of the target weekday strictly before today
        days_back = self.current_date.weekday() - python_weekday
        if days_back <= 0:
            days_back += 7
        target_date = self.current_date - timedelta(days=days_back)

        return {
            "time_reference": f"thứ {target_weekday} tuần trước",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": -days_back,
            "calculation_type": "previous_weekday"
        }

    def _convert_thu_to_python_weekday(self, thu_number: int) -> int:
        """
        Convert Vietnamese 'thứ' number to Python weekday index.
        Mapping:
        - Thứ 2 -> 0 (Monday)
        - Thứ 3 -> 1 (Tuesday)
        - Thứ 4 -> 2 (Wednesday)
        - Thứ 5 -> 3 (Thursday)
        - Thứ 6 -> 4 (Friday)
        - Thứ 7 -> 5 (Saturday)
        - Chủ nhật -> 6 (use thu_number = 8 internally)
        """
        if thu_number == 8:  # Chủ nhật
            return 6
        # thu_number expected in [2..7]
        return (thu_number - 2) % 7
        
        # Find Monday of current week
        monday_this_week = self.current_date - timedelta(days=self.current_date.weekday())
        # Subtract 7 days to get Monday of previous week
        monday_previous_week = monday_this_week - timedelta(days=7)
        # Add the target weekday offset
        target_date = monday_previous_week + timedelta(days=python_weekday)
        
        days_back = (self.current_date - target_date).days
        
        return {
            "time_reference": f"thứ {target_weekday} tuần trước",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": -days_back,
            "calculation_type": "previous_weekday"
        }
    
    def _calculate_same_day_next_month(self):
        """Calculate same day in next month"""
        try:
            next_month_date = self.current_date + relativedelta(months=1)
        except ValueError:
            # Handle edge case where next month doesn't have current day
            # Move to last day of next month
            next_month = self.current_date.replace(day=1) + relativedelta(months=1)
            next_month_date = next_month - timedelta(days=1)
        
        days_diff = (next_month_date - self.current_date).days
        
        return {
            "time_reference": "ngày này tháng sau",
            "calculated_date": next_month_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(next_month_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "next_month_same_day"
        }
    
    def _calculate_same_day_previous_month(self):
        """Calculate same day in previous month"""
        try:
            prev_month_date = self.current_date - relativedelta(months=1)
        except ValueError:
            # Handle edge case where previous month doesn't have current day
            # Move to last day of previous month
            prev_month = self.current_date.replace(day=1) - relativedelta(months=1)
            prev_month_date = prev_month - timedelta(days=1)
        
        days_diff = (prev_month_date - self.current_date).days
        
        return {
            "time_reference": "ngày này tháng trước",
            "calculated_date": prev_month_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(prev_month_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "previous_month_same_day"
        }
    
    def _calculate_same_day_next_year(self):
        """Calculate same day in next year"""
        next_year_date = self.current_date + relativedelta(years=1)
        days_diff = (next_year_date - self.current_date).days
        
        return {
            "time_reference": "ngày này năm sau",
            "calculated_date": next_year_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(next_year_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "next_year_same_day"
        }
    
    def _calculate_same_day_previous_year(self):
        """Calculate same day in previous year"""
        prev_year_date = self.current_date - relativedelta(years=1)
        days_diff = (prev_year_date - self.current_date).days
        
        return {
            "time_reference": "ngày này năm trước",
            "calculated_date": prev_year_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(prev_year_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "previous_year_same_day"
        }
    
    def _calculate_years_ahead(self, years):
        """Calculate date X years from now"""
        target_date = self.current_date + relativedelta(years=years)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": f"{years} năm nữa",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "years_ahead"
        }
    
    def _calculate_months_ahead(self, months):
        """Calculate date X months from now with proper month handling"""
        try:
            target_date = self.current_date + relativedelta(months=months)
        except ValueError:
            # Handle edge case where target month doesn't have current day
            # Move to last day of target month
            target_month = self.current_date.replace(day=1) + relativedelta(months=months)
            target_date = target_month - timedelta(days=1)
        
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": f"{months} tháng nữa",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "months_ahead"
        }
    
    def _calculate_weeks_ahead(self, weeks):
        """Calculate date X weeks from now"""
        target_date = self.current_date + timedelta(weeks=weeks)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": f"{weeks} tuần nữa",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "weeks_ahead"
        }
    
    def _calculate_days_ahead(self, days):
        """Calculate date X days from now"""
        target_date = self.current_date + timedelta(days=days)
        
        return {
            "time_reference": f"{days} ngày nữa" if days > 0 else "hôm nay",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days,
            "calculation_type": "days_ahead"
        }
    
    def _calculate_end_of_month(self):
        """Calculate last day of current month"""
        # Get last day of current month
        last_day = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        target_date = self.current_date.replace(day=last_day)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": "cuối tháng",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "end_of_month"
        }
    
    def _calculate_start_of_month(self):
        """Calculate first day of current month"""
        target_date = self.current_date.replace(day=1)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": "đầu tháng",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "start_of_month"
        }
    
    def _calculate_end_of_week(self):
        """Calculate Sunday (end of week)"""
        # Calculate days until Sunday (weekday 6)
        days_until_sunday = 6 - self.current_date.weekday()
        if days_until_sunday <= 0:  # Already Sunday or past Sunday
            days_until_sunday += 7
        
        target_date = self.current_date + timedelta(days=days_until_sunday)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": "cuối tuần",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "end_of_week"
        }
    
    def _calculate_start_of_week(self):
        """Calculate Monday (start of week)"""
        # Calculate days since Monday (weekday 0)
        days_since_monday = self.current_date.weekday()
        target_date = self.current_date - timedelta(days=days_since_monday)
        days_diff = (target_date - self.current_date).days
        
        return {
            "time_reference": "đầu tuần",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday_name(target_date.weekday()),
            "days_from_now": days_diff,
            "calculation_type": "start_of_week"
        }
    
    def _get_weekday_name(self, weekday):
        """Convert weekday number to Vietnamese name"""
        weekdays = {
            0: "Thứ 2",
            1: "Thứ 3",
            2: "Thứ 4",
            3: "Thứ 5",
            4: "Thứ 6",
            5: "Thứ 7",
            6: "Chủ nhật"
        }
        return weekdays[weekday]
    
    def get_date_info(self, time_reference):
        """
        Get comprehensive date information based on time reference
        
        Args:
            time_reference (str): Time reference text
            
        Returns:
            dict: Complete date information
        """
        return self.parse_complex_time_reference(time_reference)