def get_user_input(context):
    """
    Prompt user for input untill one of the given options is chosen
    """

    hillclimber_types = ["stochastic", "steepest"]
    optimization_type = []

    # get initialization type from user
    initialization = input(
        "Initialization type (greedy/random/cluster): ").lower()

    while initialization not in context["initialization_options"]:
        print("please try again")
        initialization = input(
            "Initialization type (greedy/random/cluster): ").lower()

    # get discrict number type from user
    district = input("District number (1/2/3): ")

    while district not in context["districts"]:
        print("please try again")
        district = input("District number (1/2/3): ")

    # user can choose whether or not houses can share gridlines
    share_grid = input(
        "Can houses share gridlines? use Prim's algorithm if so (yes/no): ").lower()

    while share_grid not in context["bools"]:
        print("please try again")
        share_grid = input("Share grid (yes/no): ").lower()

    if share_grid == "no":
        share_grid = False
    else:
        share_grid = True

    # ask user for the optimization type
    optimization = input(
        "Optimization type (none/hillclimber/simulated annealing): ").lower()

    while optimization not in context["optimization_options"]:
        print("please try again")
        optimization = input(
            "Algorithm type (none/hillclimber/simulated annealing): ").lower()

    # define which hillclimber type should be used
    if optimization == "hillclimber":
        optimization_type = input(
            "Hillclimber type (stochastic/steepest): ").lower()

        while optimization_type not in hillclimber_types:
            print("please try again")
            optimization_type = input(
                "Hillclimber type (stochastic/steepest): ").lower()

    # ask user for battery placement(advanced)
    if initialization == "cluster" and district == "3":
        advanced = True
    else:
        if initialization != "random":
            # ask user for battery placement(advanced)
            advanced = input("Place batteries (yes/no): ").lower()

            # keep prompting untull one of the options is chosen
            while advanced not in context["bools"]:
                print("please try again")
                share_grid = input("Place batteries (yes/no): ").lower()

            if advanced == "no":
                advanced = False
            else:
                advanced = True
        else:
            advanced = False

    return initialization, district, share_grid, optimization, optimization_type, advanced
