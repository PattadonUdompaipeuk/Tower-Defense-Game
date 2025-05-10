class Enemy_data:
    enemy_walk_path = ["way1,way2"]

    wave_money = [0, 150, 250, 300, 350, 400, 450, 500, 550, 600]

    enemy_wave = [
        {
            # wave1
            "Fire_bug": 5,
            "Leaf_bug": 0,
            "Magma_crab": 0
        },
        {
            # wave2
            "Fire_bug": 10,
            "Leaf_bug": 0,
            "Magma_crab": 0
        },
        {
            # wave3
            "Fire_bug": 10,
            "Leaf_bug": 5,
            "Magma_crab": 0
        },
        {
            # wave4
            "Fire_bug": 10,
            "Leaf_bug": 10,
            "Magma_crab": 0
        },
        {
            # wave5
            "Fire_bug": 12,
            "Leaf_bug": 12,
            "Magma_crab": 0
        },
        {
            # wave6
            "Fire_bug": 12,
            "Leaf_bug": 12,
            "Magma_crab": 2
        },
        {
            # wave7
            "Fire_bug": 15,
            "Leaf_bug": 15,
            "Magma_crab": 3
        },
        {
            # wave8
            "Fire_bug": 17,
            "Leaf_bug": 17,
            "Magma_crab": 4
        },
        {
            # wave9
            "Fire_bug": 20,
            "Leaf_bug": 20,
            "Magma_crab": 5
        },
        {
            # wave10
            "Fire_bug": 22,
            "Leaf_bug": 22,
            "Magma_crab": 6
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
        "money_drop": 20
    }

    magma_crab = {
        "num_width": 10,
        "num_height": 9,
        "size": (64, 64),
        "row": 8,
        "col": (3, 5),
        "health": 90,
        "speed": 2.25,
        "money_drop": 30
    }