class Enemy_data:
    enemy_walk_path = ["way1,way2"]

    wave_money = [0, 150, 250]

    enemy_wave = [
        {
            # wave1
            "Fire_bug": 5,
            "Leaf_bug": 0,
            "Magma_crab": 0
        },
        {
            # wave2
            "Fire_bug": 5,
            "Leaf_bug": 5,
            "Magma_crab": 0
        },
        {
            # wave3
            "Fire_bug": 8,
            "Leaf_bug": 3,
            "Magma_crab": 1
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
        "money_drop": 15
    }

    leaf_bug = {
        "num_width": 8,
        "num_height": 9,
        "size": (32 * 1.5, 36 * 1.5),
        "row": 8,
        "col": (3, 5),
        "health": 15,
        "speed": 4.15,
        "money_drop": 25
    }

    magma_crab = {
        "num_width": 10,
        "num_height": 9,
        "size": (64, 64),
        "row": 8,
        "col": (3, 5),
        "health": 80,
        "speed": 1.75,
        "money_drop": 30
    }