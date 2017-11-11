import sqlite3
from graph import Graph

query = (' SELECT  g.game_id as "game_id", g.game_name as "game_name", \n'
                 '                            u.user_id as "user_id", u.user_name as "user_name", \n'
                 '                            p.played_hrs as "played_hrs", r.rate as "rate"\n'
                 '                    FROM backend_playerlibrary p\n'
                 '                    INNER JOIN (\n'
                 '                        SELECT *\n'
                 '                        FROM backend_gamelist\n'
                 '                        WHERE num_player > 1\n'
                 '                        ORDER BY num_player DESC\n'
                 '                        LIMIT 504\n'
                 '                    ) g\n'
                 '                    ON g.game_id = p.game_id_id\n'
                 '                    INNER JOIN (\n'
                 '                        SELECT *\n'
                 '                        FROM (\n'
                 '                            SELECT *\n'
                 '                            FROM backend_user\n'
                 '                        ) y\n'
                 '                    ) u\n'
                 '                    ON u.user_id = p.user_id_id\n'
                 '                    LEFT JOIN backend_rating r\n'
                 '                    ON r.user_id_id = p.user_id_id\n'
                 '                    AND r.game_id_id = p.game_id_id\n'
                 '                    WHERE p.played_hrs != 0\n'
                 '                    OR p.played_hrs != null\n'
                 '                    AND p.played != 0\n'
                 '                    AND p.wish_list != 0\n;'
                 '                    ')

query2 = "SELECT user_id_id, follow_id_id FROM backend_follow;"

user_set = {}
game_set = {}
game_graph = Graph()

(account, id) = ("a regular", 76561197960530222)

def graph_init():
    conn = sqlite3.connect('mysqlite.db')
    cursor = conn.cursor()
    rows = cursor.execute(query)
    library_len = 0
    for entry in rows:
        game = entry[0]
        user = entry[2]
        rate_val = -1
        hours = entry[4]
        rate_bool = entry[5]
        if rate_bool is not None:
            rate_val = 1 if rate_bool else 0

        user_set[user] = entry[3]
        game_set[game] = entry[1]

        game_graph.connect_u_g(game, user, hours, rate_val)
        library_len += 1
    # precalculate stuff
    game_graph.add_names(user_set, game_set)
    game_graph.calculate_bias()
    # connect friends
    rows = cursor.execute(query2)
    for row in rows:
        if (row[0] not in user_set or row[1] not in user_set):
            continue
        else:
            game_graph.connect_u_u(row[0], row[1])


def main():
    graph_init()
    # find clique
    print("Num games: {}, num users: {}".format(game_graph.game_count, game_graph.user_count))
    game_graph.generate_tests()


main()
