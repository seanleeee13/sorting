import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Button, Slider
from threading import Timer
import numpy as np
import random
import math

mpl.rcParams["toolbar"] = "None"

fig = plt.figure(facecolor="black")
fig.canvas.manager.set_window_title("Bucket-Merge Sort")
ax = fig.add_subplot()
ax.patch.set_facecolor("black")

ax.spines["bottom"].set_color("black")
ax.spines["left"].set_color("black")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(colors="black")

loaded = False
length = 16
buckets = []
original_y = []

def bucket_merge_sort_data(n, a):
    mx = -math.inf
    mn = math.inf
    for val in a:
        if val < mn:
            mn = val
        if val > mx:
            mx = val
    length = mx - mn + 1
    max_pos = [-math.inf] * length
    min_pos = [math.inf] * length
    for i in range(n):
        offset_val = a[i] - mn
        if max_pos[offset_val] < i + 1:
            max_pos[offset_val] = i + 1
        if min_pos[offset_val] > i + 1:
            min_pos[offset_val] = i + 1
    x_list = []
    bucket_set = {}
    pre = -1
    set_num = 0
    for i in range(length):
        if min_pos[i] == math.inf:
            continue
        if pre != -1 and min_pos[i] < max_pos[pre]:
            x_list.append(pre + mn)
            set_num += 1
        bucket_set[i + mn] = set_num
        pre = i
    buckets = [[] for _ in range(set_num + 1)]
    for i, val in enumerate(a):
        buckets[bucket_set[val]].append(i)
    return x_list, bucket_set, buckets

def clear():
    global x_val, y_val, colors, x_list, bars, lines, original_y
    x_val = list(range(length))
    y_val = [0] * length
    colors = ["white"] * length
    x_list = []
    original_y = []
    if loaded:
        for bar, h in zip(bars, y_val):
            bar.set_height(h)
            bar.set_color("black")
        lines.set_segments([])
        fig.canvas.draw_idle()

clear()

loaded = True
bars = ax.bar(x_val, y_val, color=colors)
lines = ax.hlines(y=x_list, xmin=-1, xmax=length, colors="red", linestyles="solid", alpha=1, linewidths=min(1, 32 / length))
ax.set_xlim(-1, 16)
ax.set_ylim(0, length // 2 + 1)
is_checking = False

buc_num = 0
idx = 0
fidx = 0

def update():
    global is_running, buc_num, idx, fidx, y_val, colors, is_checking
    if not is_running:
        timer.stop()
        return
    if is_checking:
        lines.set_segments([])
        bars[fidx].set_color("lime")
        fidx += 1
        fig.canvas.draw_idle()
        if fidx >= length:
            is_running = False
    else:
        orig_idx = buckets[buc_num][idx]
        target_value = original_y[orig_idx]
        actual_idx = y_val.index(target_value, fidx)
        y_val.pop(actual_idx)
        y_val.insert(fidx, target_value)
        new_segments = [[[-1, y], [length, y]] for y in y_val]
        lines.set_segments(new_segments)
        for i, bar in enumerate(bars):
            bar.set_height(y_val[i])
            current_orig_value = y_val[i]
            matched_orig_idx = original_y.index(current_orig_value)
            bar.set_color(colors[matched_orig_idx])
        fidx += 1
        idx += 1
        if idx >= len(buckets[buc_num]):
            idx = 0
            buc_num += 1
            if buc_num >= len(buckets):
                is_checking = True
                fidx = 0
    fig.canvas.draw_idle()

timer = fig.canvas.new_timer(interval=int(1 if length >= 32 else 50))
timer.add_callback(update)
is_running = False
is_ready = False

def generate(event):
    global is_ready, y_val
    if not is_running:
        is_ready = True
        y_val = random.choices(range(1, length // 2 + 1), k=length)
        for bar, h in zip(bars, y_val):
            bar.set_height(h)
            bar.set_color("white")
        lines.set_segments([])
        fig.canvas.draw_idle()

def start(event):
    global is_running, x_list, colormap, buckets, buc_num, idx, fidx, original_y, colors, is_ready
    if not is_running and is_ready:
        is_ready = False
        is_running = True
        original_y = list(y_val)
        x_list, bucket_set, buckets = bucket_merge_sort_data(len(y_val), y_val)
        colormap = [plt.cm.gist_rainbow(i) for i in np.linspace(0, 0.85, len(buckets))]
        colors = ["white"] * length
        for i, h in enumerate(y_val):
            colors[i] = colormap[bucket_set[h]]
            bars[i].set_color(colors[i])
        new_segments = [
            [[-1, x_data], [length, x_data]]
            for x_data in x_list
        ]
        buc_num = 0
        idx = 0
        fidx = 0
        lines.set_segments(new_segments)
        fig.canvas.draw_idle()
        Timer(1.0, timer.start).start()

def reset(event):
    global is_running, is_ready, is_checking
    is_running = False
    is_ready = False
    is_checking = False
    timer.stop()
    clear()
    generate(0)

ax_button_start = plt.axes([0.3, 0.02, 0.2, 0.05])
btn_start = Button(ax_button_start, "Start", color="black", hovercolor="black")
btn_start.label.set_color("white")
btn_start.on_clicked(start)

ax_button_reset = plt.axes([0.5, 0.02, 0.2, 0.05])
btn_reset = Button(ax_button_reset, "Reset", color="black", hovercolor="black")
btn_reset.label.set_color("white")
btn_reset.on_clicked(reset)

ax_slider = plt.axes([0.45, 0.12, 0.2, 0.05])
val_slider = Slider(ax_slider, "Data Count: ", 3, 6, valinit=4, valstep=1, color="white")
val_slider.label.set_color("white")
val_slider.valtext.set_color("white")
val_slider.vline.set_visible(False)
val_slider.track.set_facecolor("black")

def update_slider_label(value):
    val_slider.valtext.set_text(value)

update_slider_label(16)

def on_change(val):
    global length, bars, lines, x_val, y_val, colors, x_list
    reset(0)
    length = int(2 ** val)
    update_slider_label(length)
    ax.clear()
    ax.set_xlim(-1, length)
    ax.set_ylim(0, length // 2 + 1)
    x_val = list(range(length))
    y_val = [0] * length
    colors = ["white"] * length
    x_list = []
    ax.patch.set_facecolor("black")
    ax.spines["bottom"].set_color("black")
    ax.spines["left"].set_color("black")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="black")
    bars = ax.bar(x_val, y_val, color=colors)
    lines = ax.hlines(y=x_list, xmin=-1, xmax=length, colors="red", linestyles="solid", alpha=1, linewidths=min(1, 32 / length))
    generate(0)

val_slider.on_changed(on_change)

generate(0)

plt.subplots_adjust(bottom=0.2)
plt.show()