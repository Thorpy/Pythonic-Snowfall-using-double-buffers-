import os
import random
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_snowflakes(ground, snowflakes, max_x, max_y):
    buffer = [[' ']*max_x for _ in range(max_y)]
    for x, y in snowflakes:
        if y < max_y:  # Ensure y is within bounds
            buffer[y][x] = '*'
    for x in range(max_x):
        for y in range(max_y - min(ground[x], max_y), max_y):  # Ensure ground[x] is within bounds
            buffer[y][x] = '*'
    return buffer

def snowfall(max_x, max_y):
    ground = [0] * max_x
    snowflakes = []

    while True:
        redraw = False

        # Dynamic snow density and speed
        density = random.uniform(0.01, 0.05)
        speed = random.uniform(0.01, 0.05)

        # Generate new snowflakes at the top
        for x in range(max_x):
            if random.random() < density:
                snowflakes.append([x, 0])
                redraw = True

        # Move snowflakes down and sideways
        new_snowflakes = []
        for x, y in snowflakes:
            new_x = x + random.choice([-3, 0, 3])  # Add some lateral movement (wind)
            new_x = max(0, min(new_x, max_x - 1))  # Stop snow "blowing" out of bounds
            new_y = y + 1 if y < max_y - ground[new_x] - 1 else y  # Ensure y is within bounds
            if new_y > y:  # If the snowflake moved down
                redraw = True
            if new_y == max_y - ground[new_x] - 1:  # If the snowflake landed
                ground[new_x] += 1
            else:
                new_snowflakes.append([new_x, new_y])
        snowflakes = new_snowflakes

        # Settle the snow
        for x in range(max_x):  # Include the first and last columns
            left_ground = ground[x - 1] if x > 0 else ground[x]  # Use the current pile for the first column
            right_ground = ground[x + 1] if x < max_x - 1 else ground[x]  # Use the current pile for the last column
            average_ground = (left_ground + ground[x] + right_ground) // 3
            if ground[x] > average_ground + 1:  # If this pile is significantly higher than its neighbours
                ground[x] -= 1  # Move some snow from this pile
                if left_ground < ground[x]:  # Move the snow to the lower neighbor
                    if x > 0:  # Avoid modifying the first column
                        ground[x - 1] += 1
                elif right_ground < ground[x]:
                    if x < max_x - 1:  # Avoid modifying the last column
                        ground[x + 1] += 1
                redraw = True

        # Draw snowflakes
        if redraw:
            buffer = draw_snowflakes(ground, snowflakes, max_x, max_y)
            clear_screen()
            for row in buffer:
                print(''.join(row))

        time.sleep(speed)

        # Break the loop when the average height of the snow piles reaches a threshold (1 being full screen)
        if sum(ground) / max_x >= max_y * 1:
            break

    return ground

def melt_snow(ground, max_x, max_y):
    # Create a copy of the ground list to avoid modifying it while iterating
    new_ground = ground.copy()

    for x in range(max_x):
        if new_ground[x] > 0:
            new_ground[x] -= 1  # Reduce the height of the snow pile

    # Draw the melting snow
    buffer = draw_snowflakes(new_ground, [], max_x, max_y)
    clear_screen()
    for row in buffer:
        print(''.join(row))

    return new_ground

def main():
    try:
        terminal_size = os.get_terminal_size()
        max_x, max_y = terminal_size.columns - 2, terminal_size.lines - 2  # Subtract 2 from both dimensions to help flickering

        while True:
            ground = snowfall(max_x, max_y)

            while max(ground) > 0:  # While there's still snow on the ground
                ground = melt_snow(ground, max_x, max_y)
                time.sleep(0.05)  # Adjust this value to control the speed of the melting effect

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
