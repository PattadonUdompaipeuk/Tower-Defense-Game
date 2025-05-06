class Enemy_data:
    enemy_walk_path = ["way1,way2"]

    wave_money = [0, 100]

    enemy_wave = [
        {
            # wave1
            "Fire_bug": 5,
            "Leaf_bug": 0,
        },
        {
            # wave2
            "Fire_bug": 10,
            "Leaf_bug": 5,
        }
    ]

    fire_bug = {
        "num_width": 11,
        "num_height": 9,
        "size": (88, 36),
        "row": 8,
        "col": (3, 5),
        "health": 30,
        "speed": 2.75,
        "money_drop": 10
    }

    leaf_bug = {
        "num_width": 8,
        "num_height": 9,
        "size": (32 * 1.5, 36 * 1.5),
        "row": 8,
        "col": (3, 5),
        "health": 15,
        "speed": 4.15,
        "money_drop": 15
    }