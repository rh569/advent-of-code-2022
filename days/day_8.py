def get_trees(input_path):
    with open(input_path) as input:
        trees: list[list[int]] = []
        lines = input.read().split('\n')
        
        for l in lines:
            trees.append(list(map(lambda x: int(x), list(l))))
        
        return trees


def part_1(input_path="input/day_8.txt"):
    trees = get_trees(input_path)

    assert len(trees) == len(trees[0])

    # outer
    t_trees = 4 * len(trees) - 4

    # inner
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees) - 1):
            height = trees[i][j]
            vis_u = True
            vis_d = True
            vis_r = True
            vis_l = True
            c_i = i
            c_j = j

            # up
            while c_i > 0:
                c_i -= 1
                if trees[c_i][j] >= height:
                    vis_u = False
            
            c_i = i

            # down
            while c_i < len(trees) - 1:
                c_i += 1
                if trees[c_i][j] >= height:
                    vis_d = False

            c_i = i

            # left
            while c_j > 0:
                c_j -= 1
                if trees[i][c_j] >= height:
                    vis_l = False

            c_j = j

            # right
            while c_j < len(trees) - 1:
                c_j += 1
                if trees[i][c_j] >= height:
                    vis_r = False
            
            if vis_u or vis_d or vis_l or vis_r:
                t_trees += 1

    return t_trees


def part_2(input_path="input/day_8.txt"):
    trees = get_trees(input_path)

    best_score = 0

    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees) - 1):

            height = trees[i][j]
            vis_u = 0
            vis_d = 0
            vis_r = 0
            vis_l = 0
            c_i = i
            c_j = j

            # up
            while c_i > 0:
                c_i -= 1
                vis_u += 1
                if trees[c_i][j] >= height:
                    break
            
            c_i = i

            # down
            while c_i < len(trees) - 1:
                c_i += 1
                vis_d += 1
                if trees[c_i][j] >= height:
                    break

            c_i = i

            # left
            while c_j > 0:
                c_j -= 1
                vis_l += 1
                if trees[i][c_j] >= height:
                    break
                
            c_j = j

            # right
            while c_j < len(trees) - 1:
                c_j += 1
                vis_r += 1
                if trees[i][c_j] >= height:
                    break

            best_score = max(best_score, vis_u * vis_d * vis_l * vis_r)

    return best_score
