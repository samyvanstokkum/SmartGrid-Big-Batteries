def get_user_input(initialization_options, districts, share_gridlines, optimization_options):
    """" Ask user for input untill one of the given options is chosen"""
    
    # define variables 
    hillclimber_types = ["stochastic", "steepest"]
    optimization_type = []

    # get initialization type from user
    initialization = input("Initialization type (greedy/random/cluster): ").lower()

    # keep prompting untull one of the options is chosen
    while initialization not in initialization_options:
        print("please try again")
        initialization = input("Initialization type (greedy/random/cluster): ").lower()

    # get discrict number type from user
    district = input("District number (1/2/3): ")    

    # keep prompting untull one of the options is chosen
    while district not in districts:
        print("please try again")
        district = input("District number (1/2/3): ") 

    # user can choose whether or not houses can share gridlines
    share_grid = input("Can houses share gridlines? use Prim's algorithm if so (yes/no): ").lower()

    # keep prompting untull one of the options is chosen
    while share_grid not in share_gridlines:
        print("please try again")
        share_grid = input("Share grid (yes/no): ").lower()
    
    if share_grid == "no":
        share_grid = False
    else:
        share_grid = True

    # ask user for the optimization type 
    optimization = input("Optimization type (none/hillclimber/simulated annealing): ").lower()

    # keep prompting untull one of the options is chosen
    while optimization not in optimization_options:
        print("please try again")
        optimization = input("Algorithm type (none/hillclimber/simulated annealing): ").lower()

    # define which hillclimber type should be used
    if optimization == "hillclimber":
        optimization_type = input("Hillclimber type (stochastic/steepest): ").lower()

        # keep prompting untull one of the options is chosen
        while optimization_type not in hillclimber_types:
            print("please try again")
            optimization_type = input("Hillclimber type (stochastic/steepest): ").lower()


    return initialization, district, share_grid, optimization, optimization_type