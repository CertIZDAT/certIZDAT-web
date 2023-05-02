from typing import Optional, Tuple


class StatsState:
    def __init__(self,
                 dataset_count_now: tuple[int, int, int],
                 gov_stats: tuple[str, str],
                 social_stats: tuple[str, str],
                 top_stats: tuple[str, str],
                 dataset_count_prev: tuple[int, int, int] = None,
                 gov_stats_prev: Optional[Tuple[str, str]] = None,
                 social_stats_prev: Optional[Tuple[str, str]] = None,
                 top_stats_prev: Optional[Tuple[str, str]] = None) -> None:
        # Actual statistics
        self.len_of_actual_gov_detected_sites = dataset_count_now[0]
        self.tuple_of_actual_gov_detected_sites = gov_stats

        self.len_of_actual_social_detected_sites = dataset_count_now[1]
        self.tuple_of_actual_social_detected_sites = social_stats

        self.len_of_gov_actual_top_detected_sites = dataset_count_now[2]
        self.tuple_of_actual_top_detected_sites = top_stats

        # Past month statistics
        self.len_of_prev_gov_detected_sites = dataset_count_prev[0]
        if gov_stats_prev is not None and len(gov_stats_prev) != 2:
            raise ValueError("Expected a tuple of two strings or None.")
        self.tuple_of_past_month_gov_detected_sites = gov_stats_prev

        self.len_of_prev_social_detected_sites = dataset_count_prev[1]
        if social_stats_prev is not None and len(social_stats_prev) != 2:
            raise ValueError("Expected a tuple of two strings or None.")
        self.tuple_of_past_month_social_detected_sites = social_stats_prev

        self.len_of_prev_top_detected_sites = dataset_count_prev[2]
        if top_stats_prev is not None and len(top_stats_prev) != 2:
            raise ValueError("Expected a tuple of two strings or None.")
        self.tuple_of_past_month_top_detected_sites = top_stats_prev

    def verify_data(self):
        # Compare past month statistics with actual, is same –> set None to 'nonable' fields.
        pass
