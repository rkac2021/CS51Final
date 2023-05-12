"""
    CS051P Final Project: Movies

    Author: Mitchell Keenan, Richard Kim

    Date:   12-8-22

    This program takes in a file on movie data sets and analyzes it in three ways: how movie budgets have changed over
    time, how profit changes based on different runtime lengths, and how global gross changes based on different genres.
"""
import matplotlib.pyplot as plt
import numpy as np

# Question 1 ----------------------------------------------------------------------------------------------------------

def extract(in_list):
    """
    Takes a list of movie parameters and returns a new list of select parameters: movie budget and date.

    :param in_list: (list) list of movie parameters
    :return: (list) list consisting of a movie's budget and its release date
    """
    # initializing list and extracting relevant elements from in_list to new list
    out_list = []
    out_list.append(in_list[-1])
    out_list.append(in_list[-9])
    return out_list


def money_format_cost(in_list):
    """
    Takes a list containing a movie's budget and its release date and converts the budget units to 100 millions of
    dollars.

    :param in_list: (list) list of a movie's budget and its release date
    :return: (list) list consisting of a movie's budget (in 100 millions of USD) and its release date
    """
    # indexing budget element
    out_list = in_list.copy()
    money = out_list[1]

    # changing units
    if money != "production_cost" and money != "NA":
        out_list[1] = str(int(money) / 100000000)
    return out_list


def parse_budget(fname):
    """
    Creates a 2D list out of a CSV file. Each sublist should represent a movie's parameters; the first element of the
    sublist should be the movie's release year and the second element should be its budget in 100 millions of dollars.

    :param fname: (string) name of the CSV file on movie data which will be passed through. Among many other parameters,
     it contains the information on production budget and release dates.
    :return: (list) 2D list in which each sublist represents a movie and contains the movie's release date and
    production costs as elements (in that respective order)
    """
    # opening file for reading and initializing empty list
    in_file = open(fname, 'r')
    budget_list = []

    # for loop extracting and cleaning up relevant data into new list
    for row in in_file:
        row_list = row.strip("\n")
        row_list = row_list.split(',')
        row_list = extract(row_list)
        row_list = money_format_cost(row_list)

        # creating sub_list of year and budget
        if row_list[0] != "NA" and row_list[1] != "NA" and row_list[1] != "production_cost":
            date_budget = (int(row_list[0]), float(row_list[1]))

            # appending sub_list to 2D list and returning
            budget_list.append(date_budget)
    return budget_list


def budget_over_time(data):
    """
    Takes in a 2D list in which each sublist contains a movie's release year and production. It points these cost-year
    pairs as a scatter plot, finds and plots a line of best fit, and labels the line of best fit.

    :param data: (list) A 2D list in which sub which each sublist contains a movie's release year and production
    """
    # initializing lists for coordinates
    time_list = []
    budget_list = []

    # organizing input data into appropriate coordinate lists
    for elem in data:
        time_list.append(elem[0])
        budget_list.append(elem[1])

    # creating arrays
    time_array = np.array(time_list)
    budget_array = np.array(budget_list)

    # finding line of best fit
    time, budget = np.polyfit(time_array, budget_array, 1)

    # plotting points
    plt.scatter(time_array, budget_array, marker='+', color="blue", label="Production Costs")

    # creating a fitted regression equation
    reg_equation = '(Production Cost) = ' + '{:.2f}'.format(budget) + ' + {:.2f}'.format(time) + '(Year)'

    # plotting line of best fit
    plt.plot(time_array, time * time_array + budget, color="red", label=reg_equation)

    # adding labels
    plt.title("Movie Production Costs Over Time")
    plt.xlabel("Year")
    plt.ylabel("Production Costs (in 100 millions of USD)")
    plt.legend()

    # save plot
    plt.savefig("Movie Production Costs Over Time")



# Question 2 ----------------------------------------------------------------------------------------------------------

def simplify(inp_list):
    """
    We transform an input list into a list consisting of three factors, the first of which is runtime, the second one is
    global revenue, and the final value is the cost of production.
    
    :param inp_list: (list) list of a movie's parameters, of which we want runtime, global revenue, and production cost.
    :return: (list) a list with a movie's runtime, global revenue, and production cost as elements
    """
    # initialize an empty list and append relevant data
    smplr_list = []
    smplr_list.append(inp_list[-2])
    smplr_list.append(inp_list[-7])
    smplr_list.append(inp_list[-9])
    return smplr_list


def parse_profit(fname):
    """
    An empty list is set up and a file is opened. At this point each row is stripped and split and a new, empty list is
    created. From this point we are verifying that there are no "NA"s present. If this is true we index these values and
    append them to the final list and return that.
    
    :param fname: (str) the filename of the movie data file
    :return: (list) a 2D list in which each sublist is filled with two values (runtime and global profit)
    """
    final_list = []
    inp_file = open(fname, 'r')
    # for every row in the input file we are removing pieces and attempting to create a list consisting of 2 elements
    for row in inp_file:
        smplr_list = simplify(row.strip("\n").split(","))
        two_list = []
        if smplr_list[0] != "NA" and smplr_list[1] != "NA" and smplr_list[2] != "NA" and smplr_list[0] != "runtime":
            two_list.append(float(smplr_list[0]))
            two_list.append(float(smplr_list[1]) - float(smplr_list[2]))
            final_list.append(two_list)
    return final_list


def new_func(final_list):
    """
    The purpose of this function is to transform features from the final_list input into pieces of a dictionary. This
    function checks whether a movies runtime falls within a key range in the t_dict and then proceeds to add one to the
    0th element of the corresponding list as well as the profit to the 1st element of the list (the value is a list).
    
    :param final_list: (list) We are using the returned list from the parse_profit function as the input for new func.
    :return: (dict) We return a modified dictionary that gives us a runtime range and the corresponding number of times
    this occurs along with the sum of the profits of the movies that fall into this range.
    """
    # initialize a runtime dict with [occurrences, total profit] values
    t_dict = {(70, 90): [0, 0], (90, 100): [0, 0], (100, 110): [0, 0], (110, 120): [0, 0], (120, 130): [0, 0],
              (130, 140): [0, 0], (140, 150): [0, 0], (150, 220): [0, 0]}

    # for each element in the final_list we are going through and checking whether the keys and adding to the lists
    for element in final_list:
        # for the range of keys in the dict we add the number of occurrences within a range plus the sum of profits
        for bucket in t_dict:
            if bucket[0] < element[0] <= bucket[1]:
                t_dict[bucket][0] += 1
                t_dict[bucket][1] += element[1]
    return t_dict


def profit_vs_runtime(data):
    """
    The first half of this function appends information we found above into two new lists. These lists are then plotted
    as a bar chart and finally titles are given to different labels and axis.
    
    :param data: (list). This is the primary/only input for the function and works along with the for statements to
    create appropriate measures to plot the data we have found.
    """
    # at this point we want to plot the keys on the x-axis and the average profits on the y-axis
    t_dict = new_func(data)

    avg_profit = []
    # here we are going through to find the average profit for the keys we have (in millions of USD)
    for occ_profit_pair in t_dict.values():
        profit = occ_profit_pair[1] / occ_profit_pair[0] / 1000000
        avg_profit.append(profit)

    runtime_groups = []
    # we are appending each key from t_dict to an empty list
    for key in t_dict:
        runtime_groups.append(str(key))

    plt.bar(runtime_groups, avg_profit)

    plt.title("Runtime vs Global Profit Averages")
    plt.xlabel("Runtime Range")
    plt.ylabel("Global Profit (in millions of USD)")
    plt.savefig("Runtime vs Global Profit Averages")


# Question 3 ----------------------------------------------------------------------------------------------------------

def money_format_gross(in_list):
    """
    Takes a list containing a movie's budget and its release date and converts the budget units to 100 millions of
    dollars.

    :param in_list: (list) list of a movie's budget and its release date
    :return: (list) list consisting of a movie's budget (in 100 millions of USD) and its release date
    """
    # indexing budget element
    out_list = in_list.copy()
    money = out_list[-7]

    # changing units
    if money != "worldwide_gross" and money != "NA":
        out_list[-7] = str(int(money) / 100000000)
    return out_list


def parse_genre(fname):
    """
    Creates a dictionary out of a CSV file. Genres make up the key, and the value for each key is a list containing the
    worldwide gross for each of the movies in said genre. The global gross will be in 100 of millions of dollars.

    :param fname: (string) name of the CSV file on movie data which will be passed through. Among many other parameters,
     it contains the information on worldwide gross and genres.
    :return: (dict) dictionary in which each key is a genre and is tied to a value that is a list. The list contains
    the global gross of each movie in the specified genre.
    """
    # opening file for reading and initializing empty list
    in_file = open(fname, 'r')
    genre_dict = {"Other": []}

    # for loop extracting and cleaning up relevant data
    for row in in_file:
        row_list = row.split(",")
        row_list = money_format_gross(row_list)

        # targeting relevant genres
        if row_list[-4] != "genre" and row_list[-4] != "NA" and row_list[-7] != "NA":
            if row_list[-4] == "Action" or row_list[-4] == "Adventure" or row_list[-4] =="Drama":

                # creating new genre keys and list values
                if row_list[-4] not in genre_dict:
                    genre_dict[row_list[-4]] = [float(row_list[-7])]
                # adding to existing keys' values
                else:
                    genre_dict[row_list[-4]].append(float(row_list[-7]))

            # sorting non-focus genres
            else:
                genre_dict["Other"].append(float(row_list[-7]))
    return genre_dict


def means(in_list):
    """
    Takes in a list and returns the mean of its elements

    :param in_list: (list) input list with numerical elements (floats)
    :return: (float) the mean of the input list's elements
    """
    # initializing variables 
    item_sum = 0
    item_count = 0
    
    # summing and counting elements
    for elem in in_list:
        item_sum += elem
        item_count += 1
    
    # returning mean
    return item_sum / item_count


def medians(in_list):
    """
    Takes in a list and returns the median of its elements
    
    :param in_list: (list) input lists with numerical elements (floats)
    :return: (float) the median of the input list's elements
    """
    # sorting list and measuring length
    in_list.sort()
    list_len = len(in_list)

    # finding and returning median
    if list_len % 2 == 0:
        center_sum = in_list[int(list_len / 2)] + in_list[int(list_len / 2) - 1]
        return center_sum / 2
    else:
        return in_list[int(list_len / 2)]


def genre_performance(data):
    """
    Takes in a dictionary in which each key is a genre and is tied to a value that is a list. The list contains
    the global gross of each movie in the specified genre. It creates boxplots for each of these genres using the data
    in each genre's respective list values.

    :param data: (dict) dictionary in which each key is a genre and is tied to a value that is a list. The list contains
    the global gross of each movie in the specified genre.
    :return: (dict) dictionary where each genre is a key and has a tuple value containing the means and medians for
    each genre's global gross data.
    """
    # initializing genre data lists
    action_data = data["Action"]
    adventure_data = data["Adventure"]
    drama_data = data["Drama"]
    other_data = data["Other"]

    # creating figure and axes instances
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)

    # creating plot
    bp = ax.boxplot([action_data, adventure_data, drama_data, other_data], notch=True, patch_artist=True,
                    showmeans=True, showfliers=True, medianprops={"color": "black", "linewidth": 0.5},
                    boxprops={"edgecolor": "black", "linewidth": 0.5},
                    whiskerprops={"color": "black", "linewidth": 1.5},
                    capprops={"color": "black", "linewidth": 1.5})

    # for loop setting colors for each boxplot
    color_set = ("lightcoral", "mediumaquamarine", "lightskyblue", "lavenderblush")
    for patch, color in zip(bp["boxes"], color_set):
        patch.set_facecolor(color)

    # labeling axes
    ax.set_xticklabels(['Action', 'Adventure',
                        'Drama', 'Other'])
    ax.set_ylabel('Global Gross (in 100 millions of USD)')
    ax.set_xlabel('Genre')
    plt.title("Worldwide Gross by Genre")

    # save plot
    plt.savefig("Worldwide Gross by Genre")

    # gather and return genre-specific data
    movie_stats = {"Action": (means(action_data), medians(action_data)),
            "Adventure": (means(adventure_data), medians(adventure_data)),
            "Drama": (means(drama_data), medians(drama_data)), "Other": (means(other_data), medians(other_data))}
    return movie_stats


# Main ----------------------------------------------------------------------------------------------------------

def main():
    """
    Takes a file on movie data and runs multiple analysis functions and data parsing functions to track movie budget
    over time, compare profits based on different runtimes, and compare global gross based on different genres. These
    functions will create a scatter plot and line of best fit for move budget over time, a bar graph for profits
    based on runtimes, and boxplots for global gross based on different genres.
    """

    # 2D tuple with analysis and data parsing functions
    analysis = ((budget_over_time, parse_budget), (profit_vs_runtime, parse_profit), (genre_performance, parse_genre))

    # running analysis functions
    for pair in analysis:
        pair[0](pair[1]("top-500-movies.csv"))
        plt.clf()


if __name__ == '__main__':
    main()