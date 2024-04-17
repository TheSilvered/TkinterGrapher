from core import GrapherBase


class Circle(GrapherBase):
    @staticmethod
    def get_param_string() -> str:
        return "(x + $a$)^2 + (y + $b$)^2 = $r$^2"

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        r = self.params["r"]

        if r == 0:
            return

        x1 = self.graph_canvas.x_plane_to_x_canvas(a - r)
        y1 = self.graph_canvas.y_plane_to_y_canvas(b - r)
        x2 = self.graph_canvas.x_plane_to_x_canvas(a + r)
        y2 = self.graph_canvas.y_plane_to_y_canvas(b + r)

        self.graph_canvas.ellipse((x1, y1), (x2, y2))


class Ellipse(GrapherBase):
    @staticmethod
    def get_param_string() -> str:
        return "(x + $c$)^2/$a$^2 + (y + $d$)^2/$b$^2 = 1"

    def graph(self):
        if not self.params.available():
            return

        a = self.params["a"]
        b = self.params["b"]
        c = self.params["c"]
        d = self.params["d"]

        if a == 0 or b == 0:
            return

        x1 = self.graph_canvas.x_plane_to_x_canvas(c - a)
        y1 = self.graph_canvas.y_plane_to_y_canvas(d - b)
        x2 = self.graph_canvas.x_plane_to_x_canvas(c + a)
        y2 = self.graph_canvas.y_plane_to_y_canvas(d + b)

        self.graph_canvas.ellipse((x1, y1), (x2, y2))
