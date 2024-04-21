from math import sqrt

from core import GrapherBase, ParamInput, InputBase


class HyperboleType1(GrapherBase):
    @staticmethod
    def get_params() -> InputBase:
        return ParamInput("(x + $c$)^2/$a$^2 - (y + $d$)^2/$b$^2 = 1")

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        c = self.params["c"]
        d = self.params["d"]

        if a == 0 or b == 0:
            return

        min_yc, max_yc = self.graph_canvas.canvas_y_range

        branch_1 = []
        branch_2 = []

        for y_canvas in range(min_yc, max_yc, -1 if min_yc > max_yc else 1):
            y = self.graph_canvas.y_canvas_to_y_plane(y_canvas)
            try:
                x1 = sqrt(a * a * ((y + d)**2 / (b*b) + 1)) - c
                x2 = -x1
            except Exception:
                continue
            x1_canvas = self.graph_canvas.x_plane_to_x_canvas(x1)
            x2_canvas = self.graph_canvas.x_plane_to_x_canvas(x2)

            branch_1.append((x1_canvas, y_canvas))
            branch_2.append((x2_canvas, y_canvas))

        self.graph_canvas.lines(branch_1)
        self.graph_canvas.lines(branch_2)


class HyperboleType2(GrapherBase):
    @staticmethod
    def get_params() -> InputBase:
        return ParamInput("(x + $c$)^2/$a$^2 - (y + $d$)^2/$b$^2 = -1")

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        c = self.params["c"]
        d = self.params["d"]

        if a == 0 or b == 0:
            return

        min_xc, max_xc = self.graph_canvas.canvas_x_range

        branch_1 = []
        branch_2 = []

        for x_canvas in range(min_xc, max_xc, -1 if min_xc > max_xc else 1):
            x = self.graph_canvas.x_canvas_to_x_plane(x_canvas)
            try:
                y1 = sqrt(b * b * ((x + c)**2 / (a*a) + 1)) - d
                y2 = -y1
            except Exception:
                continue
            y1_canvas = self.graph_canvas.y_plane_to_y_canvas(y1)
            y2_canvas = self.graph_canvas.y_plane_to_y_canvas(y2)

            branch_1.append((x_canvas, y1_canvas))
            branch_2.append((x_canvas, y2_canvas))

        self.graph_canvas.lines(branch_1)
        self.graph_canvas.lines(branch_2)
