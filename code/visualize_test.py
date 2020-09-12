from utils import Color
import matplotlib.pyplot as plt


def visualize(current_frame, candidates, auxilary, traffic_lights, traffic_auxiliary, distance):
    fig, (phase1, phase2, phase3) = plt.subplots(1, 3, figsize=(12, 6))

    phase1.set_title('phase1 results')
    phase1.imshow(current_frame.img)
    for index in range(len(candidates)):
        if auxilary[index] == Color.red:
            phase1.plot(candidates[index][0], candidates[index][1], 'r+')
        else:
            phase1.plot(candidates[index][0], candidates[index][1], 'g+')

    phase2.set_title('phase2 results')
    phase2.imshow(current_frame.img)
    for index in range(len(traffic_lights)):
        if traffic_auxiliary[index] == Color.red:
            phase2.plot(traffic_lights[index][0], traffic_lights[index][1], 'r+')
        else:
            phase2.plot(traffic_lights[index][0], traffic_lights[index][1], 'g+')

    phase3.set_title('phase3 results')
    if distance is not None:
        phase3.imshow(current_frame.img)
        for index in range(len(distance)):
            phase3.text(traffic_lights[index][0], traffic_lights[index][1], r'{0:.1f}'.format(distance[index]), color="red", fontsize=12)

    plt.show()

