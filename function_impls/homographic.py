from core import GrapherBase


class Homographic(GrapherBase):
    @staticmethod
    def get_param_string() -> str:
        return "y = ($a$x + $b$) / ($c$x + $d$)"

    def __correct_asymptote(self, points_before, points_after, asymptote):
        asymptote_canvas = self.graph_canvas.x_plane_to_x_canvas(asymptote)
        min_y, max_y = self.graph_canvas.y_range
        y_size = abs(min_y) + abs(max_y)

        if len(points_before) >= 2:
            if points_before[-2][1] > points_before[-1][1]:
                y_canvas = self.graph_canvas.y_plane_to_y_canvas(max_y + y_size)
                points_before.append((asymptote_canvas, y_canvas))
            elif points_before[-2][1] < points_before[-1][1]:
                y_canvas = self.graph_canvas.y_plane_to_y_canvas(min_y - y_size)
                points_before.append((asymptote_canvas, y_canvas))

        if len(points_after) >= 2:
            if points_after[0][1] < points_after[1][1]:
                y_canvas = self.graph_canvas.y_plane_to_y_canvas(max_y + y_size)
                points_after.insert(0, (asymptote_canvas, y_canvas))
            elif points_after[0][1] > points_after[1][1]:
                y_canvas = self.graph_canvas.y_plane_to_y_canvas(min_y - y_size)
                points_after.insert(0, (asymptote_canvas, y_canvas))

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        c = self.params["c"]
        d = self.params["d"]

        if c == 0 and d == 0:
            return

        min_cx, max_xc = self.graph_canvas.canvas_x_range

        if c != 0:
            asymptote = -d / c
        else:
            asymptote = None

        points_before = []
        points_after = []

        min_y, max_y = self.graph_canvas.y_range
        y_size = abs(min_y) + abs(max_y)

        for x_canvas in range(min_cx, max_xc, -1 if min_cx > max_xc else 1):
            x = self.graph_canvas.x_canvas_to_x_plane(x_canvas)
            try:
                y = (a * x + b) / (c * x + d)
            except ZeroDivisionError:
                continue

            if y < min_y - y_size:
                y = min_y - y_size
            elif y > max_y + y_size:
                y = max_y + y_size

            y_canvas = self.graph_canvas.y_plane_to_y_canvas(y)
            if asymptote is not None and x > asymptote:
                points_after.append((x_canvas, y_canvas))
            else:
                points_before.append((x_canvas, y_canvas))

        if asymptote is not None:
            self.__correct_asymptote(points_before, points_after, asymptote)

        if points_before:
            self.graph_canvas.lines(points_before)
        if points_after:
            self.graph_canvas.lines(points_after)
