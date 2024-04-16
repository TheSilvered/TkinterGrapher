from core.grapher_base import GrapherBase


class LineType1(GrapherBase):
    @staticmethod
    def get_param_string():
        return "y = $m$x + $q$"

    def graph(self):
        if not self.params.available():
            return

        m = self.params["m"]
        q = self.params["q"]

        min_x, max_x = self.graph_canvas.x_range
        y1 = min_x * m + q
        y2 = max_x * m + q
        y1_canvas = self.graph_canvas.y_plane_to_y_canvas(y1)
        y2_canvas = self.graph_canvas.y_plane_to_y_canvas(y2)
        self.graph_canvas.line(
            (self.graph_canvas.canvas_x_range[0], y1_canvas),
            (self.graph_canvas.canvas_x_range[1], y2_canvas)
        )


class LineType2(GrapherBase):
    @staticmethod
    def get_param_string():
        return "$a$x + $b$y + $c$ = 0"

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        c = self.params["c"]

        if a == b == 0:
            return

        if b == 0:
            x_canvas = self.graph_canvas.x_plane_to_x_canvas(-c)
            self.graph_canvas.line(
                (x_canvas, self.graph_canvas.canvas_y_range[0]),
                (x_canvas, self.graph_canvas.canvas_y_range[1])
            )
        else:
            m = -a / b
            q = -c / b
            min_x, max_x = self.graph_canvas.x_range
            y1 = min_x * m + q
            y2 = max_x * m + q
            y1_canvas = self.graph_canvas.y_plane_to_y_canvas(y1)
            y2_canvas = self.graph_canvas.y_plane_to_y_canvas(y2)
            self.graph_canvas.line(
                (self.graph_canvas.canvas_x_range[0], y1_canvas),
                (self.graph_canvas.canvas_x_range[1], y2_canvas)
            )
