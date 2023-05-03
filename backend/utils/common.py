from sqlite3 import Connection

from utils import db

from utils.StatsState import StatsState


def get_total_stats(connection: Connection) -> StatsState:
    dataset_count_now: tuple[int, int, int] = (connection.execute(db.get_stats_count('gov', 'now')).fetchone(),
                                               connection.execute(db.get_stats_count('social', 'now')).fetchone(),
                                               connection.execute(db.get_stats_count('top', 'now')).fetchone())
    # Get the tuple of the 'Russian Trusted CA' and self-signed sites
    gov_stats: tuple[str, str] = (connection.execute(db.get_list_of('gov', 'ca', 'now')).fetchone(),
                                  connection.execute(db.get_list_of('gov', 'ss', 'now')).fetchone())

    social_stats: tuple[str, str] = (connection.execute(db.get_list_of('social', 'ca', 'now')).fetchone(),
                                     connection.execute(db.get_list_of('social', 'ss', 'now')).fetchone())

    top_stats: tuple[str, str] = (connection.execute(db.get_list_of('top', 'ca', 'now')).fetchone(),
                                  connection.execute(db.get_list_of('top', 'ss', 'now')).fetchone())

    dataset_count_prev: tuple[int, int, int] = (connection.execute(db.get_stats_count('gov', 'prev')).fetchone(),
                                                connection.execute(db.get_stats_count('social', 'prev')).fetchone(),
                                                connection.execute(db.get_stats_count('top', 'prev')).fetchone())

    gov_stats_prev: tuple[str, str] = (connection.execute(db.get_list_of('gov', 'ca', 'prev')).fetchone(),
                                       connection.execute(db.get_list_of('gov', 'ss', 'prev')).fetchone())
    social_stats_prev: tuple[str, str] = (connection.execute(db.get_list_of('social', 'ca', 'prev')).fetchone(),
                                          connection.execute(db.get_list_of('social', 'ss', 'prev')).fetchone())
    top_stats_prev: tuple[str, str] = (connection.execute(db.get_list_of('top', 'ca', 'prev')).fetchone(),
                                       connection.execute(db.get_list_of('top', 'ss', 'prev')).fetchone())

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
