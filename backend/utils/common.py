from sqlite3 import Connection

from utils import db

from backend.utils.StatsState import StatsState


def get_total_stats(connection: Connection) -> StatsState:
    dataset_count_now: tuple[int, int, int] = (connection.execute(db.get_stats_count('gov', 'now')).fetchone(),
                                               connection.execute(db.get_stats_count('social', 'now')).fetchone(),
                                               connection.execute(db.get_stats_count('top', 'now')).fetchone())
    # Get the tuple of the 'Russian Trusted CA' and self-signed sites
    gov_stats: tuple[str, str] = (connection.execute(db.get_list_of('gov', 'ca')).fetchone(),
                                  connection.execute(db.get_list_of('gov', 'ss')).fetchone())

    social_stats: tuple[str, str] = (connection.execute(db.get_list_of('social', 'ca')).fetchone(),
                                     connection.execute(db.get_list_of('social', 'ss')).fetchone())

    top_stats: tuple[str, str] = (connection.execute(db.get_list_of('top', 'ca')).fetchone(),
                                  connection.execute(db.get_list_of('top', 'ss')).fetchone())

    dataset_count_prev: tuple[int, int, int] = (connection.execute(db.get_stats_count('gov', 'prev')).fetchone(),
                                                connection.execute(db.get_stats_count('social', 'prev')).fetchone(),
                                                connection.execute(db.get_stats_count('top', 'prev')).fetchone())
    gov_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()
    social_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()
    top_stats_prev: tuple[str] = connection.execute(db.get_gov_stats_for_prev_month).fetchone()

    state = StatsState(dataset_count_now=dataset_count_now,
                       gov_stats=gov_stats,
                       social_stats=social_stats,
                       top_stats=top_stats,
                       dataset_count_prev=dataset_count_prev,
                       gov_stats_prev=gov_stats_prev,
                       social_stats_prev=social_stats_prev,
                       top_stats_prev=top_stats_prev)

    state.verify_data()
    return state


def get_latest_list_results(connection, ssl_case: str = 'CA') -> str:
    # Get list of CA and self-signed
    if ssl_case == 'CA':
        return __clean_db_response(connection.execute(
            db.get_last_ca_list).fetchall()[0][0])
    else:
        response = connection.execute(
            db.get_last_self_sign_list).fetchall()[0][0]
        items = [item.strip() for item in str(response).split(",")]
        return "\n".join([item for item in items])


def __clean_db_response(response) -> str:
    items = [item.strip() for item in str(response).split(",")]
    return "\n".join(
        [str(item[0]).strip("(),") if isinstance(item, tuple) and len(item) == 1 else item.split(' ')[0] for item in
         items])
