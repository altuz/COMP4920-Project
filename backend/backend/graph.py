import math
import numpy as np
import random

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
        # Global average number of hours per user
        self.average_hoursNorm = 0

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

    # add connection between user one to user two
    def connect_u_u(self, u1, u2):
        # find indices
        if u1 not in self.uid_lookup:
            return
        if u2 not in self.uid_lookup:
            return
        u1_idx = self.uid_lookup[u1]
        # u2_idx = self.uid_lookup[u2]
        # get nodes
        u1_node = self.u_nodes[u1_idx]
        # make u1 follow u2
        u1_node.follow_list.append(u2)

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
        #global average rating
        rating_total = 0
        rating_count = 0
        for user in self.u_nodes:
            for edge in user.edges:
                if edge.rating is -1:
                    continue
                rating_total += edge.rating
                rating_count += 1
        return float(rating_total)/rating_count

    def calculate_bias(self):
        print("Calculating bias & global average")
        global_total_hoursNorm = 0
        global_num_users = 0
        for game in self.g_nodes:
            game.average_weight()
            game.calcHoursNorm()
            global_total_hoursNorm += game.total_hoursNorm
            global_num_users += game.num_users
            # print("game {} has averages of ({} hours, {} rating)".format(self.gid_names[game.node_id], game.average_hours, game.average_rating))

        self.average_hoursNorm = global_total_hoursNorm/global_num_users
        print("Global average is" + str(self.average_hoursNorm))

        num_reviews = []
        for user in self.u_nodes:
            user.average_weight()
            num_reviews.append(str(user.num_rating))
            # print("user {} has averages of ({} hours, {} rating)".format(self.uid_names[user.node_id], user.average_hours, user.average_rating))
        # num_reviews = sorted(num_reviews)
        # print(', '.join(num_reviews))

    # Gets random user from list of users
    # A misnomer, it will be changed to get user's friends first, and their friends. BFS till num
    # XD
    def get_random_usernodes(self, user_id, num):
        visited = set()
        visited.add(user_id)
        queue = [user_id]
        random_users = []
        count = 0
        while queue is not [] and count < num + 1:
            if len(queue) is 0:
                break;
            curr_user = queue.pop()
            curr_user_node = self.u_nodes[self.uid_lookup[curr_user]]
            count += 1
            random_users.insert(0, curr_user_node)
            for friend in curr_user_node.follow_list:
                if friend not in visited:
                    visited.add(friend)
                    queue.insert(0, friend)
        print("Count users: " + str(count))
        user_node = self.u_nodes[self.uid_lookup[user_id]]
        if count < num + 1:
            print("HERE")
            copy_u = set(self.u_nodes)
            copy_u.remove(user_node)
            random_users = random.sample(copy_u, (num + 1 - count)) + random_users

        #random_users = random.sample(self.u_nodes, num)
        return random_users

    def baseline_predictor(self, user_id, num):
        random_users = self.get_random_usernodes(user_id, num)
        random_users.append(self.u_nodes[self.uid_lookup[user_id]])
        ruser_count = num + 1
        global_ave = self.average_hoursNorm
        matrix = []
        ratings = []
        i = 0
        for user in random_users:
            uid = user.node_id
            for edge in user.edges:
                #if edge.rating is -1:
                #    continue
                vector = [0 for col in range(ruser_count + self.game_count)]
                gid = edge.game.node_id
                uidx = i
                gidx = self.gid_lookup[gid]
                # user comes first
                vector[uidx] = 1
                vector[ruser_count + gidx] = 1
                matrix.append(vector)
                ratings.append([edge.hoursNorm - global_ave])
            i += 1
        # build numpy array
        print()
        print("global ave is " + str(global_ave))
        a = np.matrix(matrix)
        b = np.matrix(ratings)
        # calculate least squares of first derivative
        # at = np.matrix.transpose(a)
        b = np.matmul(a.T, b)
        a = np.matmul(a.T, a)
        c = np.linalg.lstsq(a, b)
        # self.show_baseline(c)
        predictions = self.get_recommendation(user_id, c, num)
        predictionList = []
        for tuple in predictions:
            gid = self.g_nodes[tuple[0]].node_id
            rating = tuple[1]
            gamename = self.gid_names[gid]
            predictionList.append([gid,rating])
            print("Game {} is predicted to have rating of {}".format(gamename, rating))
        # return predictions
        return predictionList

    def show_baseline(self, result):
        solution = result[0]
        residuals = result[1]
        rank = result[2]
        singular = result[3]
        print("Solution = {}".format(", ".join("{0}".format(n) for n in solution.T)))
        # print("Residual = {}".format(", ".join("{0}".format(n) for n in residuals)))
        print("Rank is " + str(rank))

    def get_recommendation(self, user_id, result, count):
        all_biases = result[0]
        predicted_rating = []
        global_ave = self.average_hoursNorm
        uidx = count
        print("Length is " + str(len(all_biases)))
        print("There are {} games and {} users".format(self.game_count, count + 1))
        for game_id in range(self.game_count):
            prediction = global_ave + all_biases[uidx, 0] + all_biases[count + game_id, 0]
            predicted_rating.append([game_id, prediction])

        sorted_prediction = sorted(predicted_rating, key = lambda tuple : tuple[1], reverse = False)
        return sorted_prediction

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
        # number of reviews
        self.num_rating = 0
        # fields to be used for global average calc
        self.total_hoursNorm = 0
        self.num_users = 0
        # follow list
        self.follow_list = []

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
            if edge.rating is not -1:
                total_rating += edge.rating
                rating_count += 1
        self.num_rating = rating_count
        self.average_hours = float(total_hours)/len(self.edges)
        self.average_rating = float(total_rating)/rating_count if rating_count is not 0 else -1

    # Call for GAME nodes only, updates each edges normalised hrs value
    def calcHoursNorm(self):
        max = 0
        self.num_users = 0
        self.total_hoursNorm = 0
        for edge in self.edges:
            edge.hoursNorm = math.atan(edge.hours/(self.average_hours))
            if(edge.hoursNorm > max):
                max = edge.hoursNorm
            # print("------------edge hr: " + str(edge.hours) + ", node ave hr:" + str(self.average_hours) + " atanHr:" + str(edge.hoursNorm))
        # TODO not sure if need to scale even, since going to use for ranking
        # Scale according to the max so that value ranges are between 0 and 1
        for edge in self.edges:
            old = edge.hoursNorm
            edge.hoursNorm = old / max

            self.num_users += 1 # Number of outgoing edges equates to number of users
            self.total_hoursNorm += edge.hoursNorm # keep track of total hoursNorm
            # print("------Adjusted-----edge hr: " + str(edge.hours) + ", node ave hr:"
            #       + str(self.average_hours) + " atanHr:" + str(edge.hoursNorm) + ", max: " + str(max))
        print("For game" + str(self.node_id) + " total users = " + str(self.num_users) 
            + ", total_hoursNorm = " + str(self.total_hoursNorm))

class Edge:
    # define an edge between two nodes
    def __init__(self, g_node, u_node, hours, rating):
        self.game = g_node
        self.user = u_node
        self.hours = hours
        self.rating = rating
        self.hoursNorm = -1 # Normalised hrs, -1 means has not been computed yet

