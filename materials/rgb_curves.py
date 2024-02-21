import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.backend_bases import MouseButton
from copy import deepcopy
from scipy.interpolate import RBFInterpolator
from scipy import interpolate

is_it = False
is_add = False
in_points = [0, 0.25, 0.75, 1]
out_points = [0, 0.25, 0.75, 1]


def rgb_curve():
    poly = interpolate.PchipInterpolator(in_points, out_points)  # Akima1DInterpolator PchipInterpolator
    # poly=make_interp_spline(in_points,out_points)
    # poly=np.polynomial.polynomial.Polynomial.fit(in_points,out_points,9)
    draw_x = np.linspace(0, 1, 100)
    draw_y = poly(draw_x)
    # poly2 = make_interp_spline(draw_x, draw_y)
    # draw_y = poly2(draw_x)

    fig, ax = plt.subplots()
    ax.plot(draw_x, draw_y)
    ax.plot(in_points, out_points, 'o')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    def on_move(event):
        global in_points, out_points, is_it, is_add
        if is_it == True:
            if event.inaxes:
                if event.xdata != any(in_points):
                    if is_add == True:
                        del in_points[-1]
                        del out_points[-1]
                    in_points.append(event.xdata)
                    out_points.append(event.ydata)
                    redraw()
                    print(event.xdata)
                    is_add = True

            # print(f'data coords {event.xdata} {event.ydata},',
            #     f'pixel coords {event.x} {event.y}')

    def redraw():
        global in_points, out_points
        in_t = deepcopy(in_points)
        out_t = deepcopy(out_points)
        in_t.sort()
        out_t.sort()
        poly = interpolate.PchipInterpolator(in_t, out_t)
        # poly=make_interp_spline(in_t,out_t)
        # poly=np.polynomial.polynomial.Polynomial.fit(in_points,out_points,9)
        draw_x = np.linspace(0, 1, 100)
        draw_y = poly(draw_x)
        poly2 = make_interp_spline(draw_x, draw_y, k=1)
        draw_y = poly2(draw_y)
        draw_y[draw_y > 1] = 1
        draw_y[draw_y < 0] = 0
        ax.clear()
        ax.plot(in_t, out_t, 'o')
        ax.plot(draw_x, draw_y)
        ax.set_xlim(0., 1.)
        ax.set_ylim(0., 1.)
        fig.canvas.draw()

    def on_click(event):
        global in_points, out_points, is_it, is_add
        if event.button is MouseButton.LEFT:
            is_it = not is_it
            if is_it == True:
                is_add = False

                for i in range(len(out_points)):
                    print(abs(event.xdata - in_points[i]), "oouuu", i)
                    if abs(event.xdata - in_points[i]) < 0.01:
                        del in_points[i]
                        del out_points[i]
                        redraw()
        if event.button is MouseButton.RIGHT:
            for i in range(len(out_points)):
                print(abs(event.xdata - in_points[i]), "oouuu", i)
                if abs(event.xdata - in_points[i]) < 0.01:
                    del in_points[i]
                    del out_points[i]
                    redraw()

    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)
    plt.show()

    return plt

rgb_curve()
