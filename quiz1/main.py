def main():
    ListWithSubList = ["1", "2", "3"]

    def create_combinations(lst):
        if len(lst) == 0:
            return [[]]
        first = lst[0]
        rest_combinations = create_combinations(lst[1:])
        with_first = [[first] + combination for combination in rest_combinations]
        return with_first + rest_combinations

    combinations = create_combinations(ListWithSubList)
    for combo in combinations:
        print(combo)

if __name__ == "__main__":
    main()
