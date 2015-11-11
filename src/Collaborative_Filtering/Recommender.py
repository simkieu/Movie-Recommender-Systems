from math import sqrt
import csv
from operator import itemgetter, attrgetter, methodcaller
import sys

class UserBasedCF:

    def __init__(self):
        pass

#This function generates the movie adjacency list
    def adj_gen_movie(self, file_name):
        input_file = open(file_name, 'r');
        csv_file = csv.reader(input_file);
        movie_adjList = {};

        for row in csv_file:
            movie = int(row[1]);
            user = int(row[0]);
            rating = int(row[2]);
            if not movie in movie_adjList:
                movie_adjList[movie] = {user: rating}
            else:
                movie_adjList[movie].update({user: rating})
        
        input_file.close()
        return movie_adjList


#This function generates the movie adjacency list for cross validation
    def adj_gen_movie_cv(self, train_set):
        movie_adjList = {};
        for row in train_set:
            movie = row[1];
            user = row[0];
            rating = row[2];
            if not movie in movie_adjList:
                movie_adjList[movie] = {user: rating};
            else:
                movie_adjList[movie].update({user: rating});
        return movie_adjList;


#This function calculates Pearson distance between two users
    def pearson(self, rating1, rating2):
        sum_xy = 0;
        sum_x = 0;
        sum_y = 0;
        sum_x2 = 0;
        sum_y2 = 0;
        n = 0;
        for key in rating1:
            if key in rating2:
                n += 1;
                x = rating1[key];
                y = rating2[key];
                sum_xy += x * y;
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n) 
                        * sqrt(sum_y2 - pow(sum_y, 2) / n));
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator;


#This function finds the nearest neighbors based on pearson correlation values
    def find_nn_pearson(self, username, users):
        distances = [];
        distance = 0;
        for key in users:
            if (key != username):
                distance = self.pearson(users[username], users[key]);
                if distance >= 0:
                    distances.append((key, distance));
        return sorted(distances, key = itemgetter(1), reverse = True);


#This function predicts missing ratings for users
    def predictRating(self, user, movie, users, neighbors):
        sum_ratings_user = 0;
        rating_counter = 0;
        avg_user_rating = 0.0;
        sum_ratings_similarities = 0.0;
        sum_similarity = 0.0;

        #this part calculates user's rating average
        user_ratings = users[user];
        for key in user_ratings:
            sum_ratings_user += user_ratings[key];
            rating_counter += 1;
        if (sum_ratings_user > 0):
            avg_user_rating = sum_ratings_user / rating_counter;
        
        #this part calculates neighbor sum of similarities and sum of similarity ratings product
        count_neighbors = 1;
        for neighbor in neighbors:
            if (count_neighbors < 21):
                neighbor_ratings = users[neighbor[0]];
                sum_neighbor_rating = 0;
                avg_neighbor_rating = 0.0;
                counter = 0;
                if movie in neighbor_ratings:
                    sum_similarity += abs(neighbor[1]);
                    count_neighbors += 1;
                    for key in neighbor_ratings:
                        sum_neighbor_rating += neighbor_ratings[key];
                        counter += 1;
                    if sum_ratings_user > 0:
                        avg_neighbor_rating = sum_neighbor_rating / counter;
                    sum_ratings_similarities += neighbor[1] * (neighbor_ratings[movie] - avg_neighbor_rating)
        
        if sum_similarity > 0:
            newrating = avg_user_rating + sum_ratings_similarities / sum_similarity;
        else:
            return 0;
        if newrating >= 5:
            newrating = 5;
        elif newrating <= 1:
            newrating = 1;
        return newrating;


    def cross_validation(self, method, metric, input_name):
        rmse_arr = [];
        for fold in range(3, 11):
            rmse = [];
            for i in range(1, fold + 1):
                train = [];
                test = [];
                ground_truth = [];
                with open(input_name, 'r') as csvinput:
                    reader = csv.reader(csvinput);
                    train_counter = 1;
                    test_counter = i;
                    for row in reader:
                        if (train_counter == test_counter):
                            test.append((int(row[0]), int(row[1]), float(row[2])));
                            ground_truth.append((int(row[0]), int(row[1]), float(row[2])));
                            test_counter += fold;
                            train_counter += 1;
                        else:
                            train.append((int(row[0]), int(row[1]), float(row[2])));
                            train_counter += 1;
                    csvinput.close();

                    m_adj_list_cv = {};
                    m_adj_list_cv = self.adj_gen_movie_cv(train);
                    predictions = [];

                    if (method == "Item") and (metric == "Pearson"):
                        pearson_neighbor_set = {}
                        for row in test:
                            newrating = 0.0;
                            newuser = row[0];
                            newmovie = row[1];
                            if newmovie in m_adj_list_cv:
                                if newmovie in pearson_neighbor_set:
                                    newrating = self.predictRating(newmovie, newuser, m_adj_list_cv,
                                        pearson_neighbor_set[newmovie]);
                                else:
                                    pearson_neighbor_set[newmovie] = self.find_nn_pearson(newmovie, m_adj_list_cv)
                                    if len(pearson_neighbor_set[newmovie]) > 0:
                                        newrating = self.predictRating(newmovie, newuser, m_adj_list_cv,
                                            pearson_neighbor_set[newmovie]);
                                    else:
                                        newrating = 3;
                            predictions.append(newrating);
                        
                        counter = 0;
                        squared_error = 0.0;
                        for row in test:
                            squared_error += pow((predictions[counter] - row[2]), 2);
                            counter += 1;
                        rmse.append(pow((squared_error / counter), 0.5));
                        print(rmse, len(test));

            rmse_arr.append(sum(rmse) / len(rmse))
            print(sum(rmse) / len(rmse));
        
        with open("rmse-user-pearson.csv", "w") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator = "\n");
            cnt = 2;
            for val in rmse_arr:
                cnt += 1;
                writer.writerow((cnt, val));
        csvoutput.close();


def main():
    
    continue_running = True;
    # while continue_running:
    # connecting = False;
    item_based = True;
    pearson_metric = True;
    cross_validation = True;

    test = UserBasedCF();

    if (cross_validation) and (item_based) and (pearson_metric):
        test.cross_validation("Item", "Pearson", "_data.csv");


if __name__ == '__main__':
    main()
  