# Bipartite graph between set of users and set of games
class Graph:
    # define empty graph
    def __init__(self):
        self.user_count = 0
        self.game_count = 0
        # dict to lookup user/games to their index in set
        self.uid_lookup = {}
        self.gid_lookup = {}
        # set of games and users
        self.g_nodes = []
        self.u_nodes = []
        #
        self.uid_names = None
        self.gid_names = None

    # add user, returns true if added, false if user already in list
    def add_user(self, uid):
        if uid in self.uid_lookup:
            return False
        new_user = Node(True, uid)
        self.u_nodes.append(new_user)
        self.uid_lookup[uid] = self.user_count
        self.user_count += 1
        return True

    # add game, returns true if added, false if game already in list
    def add_game(self, gid):
        if gid in self.gid_lookup:
            return False
        new_game = Node(False, gid)
        self.g_nodes.append(new_game)
        self.gid_lookup[gid] = self.game_count
        self.game_count += 1
        return True

    # add connection between user and game
    def connect_u_g(self, gid, uid, hrs, rt):
        # Check if user - game pair in graph
        if uid not in self.uid_lookup:
            self.add_user(uid)
        if gid not in self.gid_lookup:
            self.add_game(gid)
        # Get their index in graph
        g_idx = self.gid_lookup[gid]
        u_idx = self.uid_lookup[uid]
        # Get the actual nodes
        g_node = self.g_nodes[g_idx]
        u_node = self.u_nodes[u_idx]
        # Create a new edge
        g_u_edge = Edge(g_node, u_node, hrs, rt)
        # We don't have to check if connection exist since it is guaranteed to be unique
        g_node.add_edge(g_u_edge)
        u_node.add_edge(g_u_edge)
        return True

    # add a dictionary of names
    def add_names(self, unames, gnames):
        self.uid_names = unames
        self.gid_names = gnames
    # calculate stats for games
    def games_hours_stats(self):
        print("there are {} games".format(len(self.g_nodes)))
        for game in self.g_nodes:
            if len(game.edges) < 5:
                continue
            print("Stat for Game: {}({})".format(self.gid_names[game.node_id], game.node_id))
            if not game.hours_stat:
                game.categorize_hours()
            print("This game has {} players".format(len(game.edges)))
            print("Cut Offs: {}, {}, {}, {}, {}".format(game.hours_stat[0], game.hours_stat[1], game.hours_stat[2],
                                                        game.hours_stat[3], game.hours_stat[4]))

    def calculate_average(self):
        ""

    def calculate_bias(self):
        print("Calculating bias ")
        for game in self.g_nodes:
            game.average_weight()
            print("game {} has averages of ({} hours, {} rating)".format(self.gid_names[game.node_id], game.average_hours, game.average_rating))

        for user in self.u_nodes:
            user.average_weight()
            print("user {} has averages of ({} hours, {} rating)".format(self.uid_names[user.node_id], user.average_hours, user.average_rating))


class Node:
    # define a new node
    def __init__(self, nt, nid):
        self.node_type = nt
        self.node_id = nid
        self.edges = []
        self.hours_stat = []
        # averages
        self.average_hours = 0
        self.average_rating = 0

    def add_edge(self, h):
        self.edges.append(h)

    # don't call this function on a user.
    # as it won't make sense
    # this data is only useful across individual games
    # To categorize users we have to do this for every game and cross check it with users
    def categorize_hours(self):
        sorted_hours = sorted(self.edges, key = lambda edge : edge.hours, reverse = False)
        num_edges = len(sorted_hours)
        # Convert it to rating based on every 20th percentile
        for i in range(0, 5):
            edge_idx = int((float(num_edges) / 5) * (i + 1)) - 1
            # print("{}th percentile is cut off at {} hours played".format(20 * (i + 1), sorted_edges[edge_idx].weight))
            self.hours_stat.append(sorted_hours[edge_idx].hours)

    def average_weight(self):
        total_hours = 0
        total_rating = 0
        rating_count = 0
        for edge in self.edges:
            total_hours += edge.hours
            if edge.rating is not 0:
                total_rating += edge.rating
                rating_count += 1
        self.average_hours = float(total_hours)/len(self.edges)
        self.average_rating = float(total_rating)/rating_count if rating_count is not 0 else None

class Edge:
    # define an edge between two nodes
    def __init__(self, g_node, u_node, hours, rating):
        self.game = g_node
        self.user = u_node
        self.hours = hours
        self.rating = rating