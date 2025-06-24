from collections import defaultdict


def merge_variations(variations: list[list[str]]) -> list:
    tree = defaultdict(list)

    for path in variations:
        if not path:
            continue
        first_move, rest = path[0], path[1:]
        tree[first_move].append(rest)

    merged = []
    for move, branches in tree.items():
        # Recursively merge each set of sub-branches
        if not move:
            continue
        children = merge_variations(branches)
        merged.append([move, children] if children else [move])

    return merged


def variations_to_sgf(tree, player):
    def opposite(p):
        return "W" if p == "B" else "B"

    def build(nodes, current_player):
        sgf = ""
        for node in nodes:
            move = node[0]
            children = node[1] if len(node) > 1 else []
            sgf += f";{current_player}[{move}]"

            # Single child path: write it inline
            while len(children) == 1:
                next_node = children[0]
                next_move = next_node[0]
                sgf += f";{opposite(current_player)}[{next_move}]"
                children = next_node[1] if len(next_node) > 1 else []
                current_player = opposite(current_player)

            # Multiple children: variations
            if len(children) > 1:
                for child in children:
                    sgf += f"({build([child], opposite(current_player))})"

        return sgf

    return build(tree, player)


# variations = [["es", "ds", "fs"], ["es", "fs", "gs"]]
# tree = merge_variations(variations)
# print(variations_to_sgf(tree, "B"))
