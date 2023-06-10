import math
from TuioPatterns import TuioGestures, Point2D, GestureTemplate


class GeometricRecognizer:
    def __init__(self):
        self.TuioGestures = TuioGestures()

        self.HalfDiagonal: float = 0
        self.AngleRange: float = 0
        self.AnglePrecision: float = 0
        self.GoldenRatio: float = 0
        self.NumPointsInGesture: float = 0
        self.SquareSize: float = 0
        self._shouldIgnoreRotation: bool = False
        self.Templates: list() = []

        self.RotationInvariance: bool = False
        self.AngleRange: float = 45.0 if self._shouldIgnoreRotation else 15.0

        self.NumPointsInGesture: int = 128
        self.SquareSize: int = 250
        self.HalfDiagonal: float = 0.5 * math.sqrt((250.0 * 250.0) + (250.0 * 250.0))
        self.RotationInvariance: bool = False
        self.AnglePrecision: float = 2.0
        self.GoldenRatio: float = 0.5 * (-1.0 + math.sqrt(5.0))
        self.load_templates()

    @property
    def RotationInvariance(self):
        return self._shouldIgnoreRotation

    @RotationInvariance.setter
    def RotationInvariance(self, value: float):
        self._shouldIgnoreRotation = value
        self.AngleRange = 45.0 if self._shouldIgnoreRotation else 15.0

    def load_templates(self):
        for template in TuioGestures.templates:
            self.Templates.append(
                GestureTemplate(template.Name, self.normalize_path(template.Path))
            )

    def recognize(self, points: list):
        if not self.Templates:
            print("No templates loaded, so no symbols to match.")
            return RecognitionResult("Unknown", 1)

        points = self.normalize_path(points)
        best_distance = float("inf")
        best_template = None

        for template in self.Templates:
            distance = self.distance_at_best_angle(points, template)
            if distance < best_distance:
                best_distance = distance
                best_template = template

        score = 1.0 - (best_distance / self.HalfDiagonal)

        if best_template is None:
            return RecognitionResult("Unknown", 1)

        best_match = RecognitionResult(best_template.Name, score)
        return best_match


    # ===============================================================================
    # UTIL
    def normalize_path(self, points: list):
        points = self.resample(points)

        if self.RotationInvariance:
            points = self.rotate_to_zero(points)

        points = self.scale_to_square(points)
        points = self.translate_to_origin(points)
        return points

    def translate_to_origin(self, points: list()):
        c = self.controid(points)
        newPoints = []
        for point in points:
            qx = point.x - c.x
            qy = point.y - c.y
            newPoints.append(Point2D(qx, qy))
        return newPoints

    def scale_to_square(self, points: list()):
        box = self.calc_bounding_box(points)
        newPoints = []
        if (box.Width == 0) or (box.Height == 0):
            return newPoints
        
        for point in points:
            scaledX = point.x * (self.SquareSize / box.Width)
            scaledY = point.y * (self.SquareSize / box.Height)
            newPoints.append(Point2D(scaledX, scaledY))
        return newPoints

    def calc_bounding_box(self, points: list()):
        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")

        for point in points:
            if point.x < minX:
                minX = point.x
            if point.x > maxX:
                maxX = point.x
            if point.y < minY:
                minY = point.y
            if point.y > maxY:
                maxY = point.y

        return Rectangle(minX, minY, maxX - minX, maxY - minY)

    def rotate_to_zero(self, points: list()):
        c = self.controid(points)
        rotation = math.atan2(c.y - points[0].y, c.x - points[0].x)
        points = self.rotate_by(points, -rotation)
        return points

    def rotate_by(self, points: list(), rotation: float):
        controid = self.controid(points)
        cos = math.cos(rotation)
        sin = math.sin(rotation)
        newPoints = []

        for point in points:
            qx = (
                (point.x - controid.x) * cos - (point.y - controid.y) * sin + controid.x
            )
            qy = (
                (point.x - controid.x) * sin + (point.y - controid.y) * cos + controid.y
            )
            newPoints.append(Point2D(qx, qy))

        return newPoints

    def controid(self, points: list()):
        x = 0.0
        y = 0.0

        for point in points:
            x += point.x
            y += point.y

        if len(points) == 0:
            return Point2D(0, 0)
        
        x /= len(points)
        y /= len(points)
        return Point2D(x, y)

    def resample(self, points: list):
        interval = self.path_length(points) / (self.NumPointsInGesture - 1)
        d = 0.0
        newPoints = [points[0]]

        i = 1
        while i < len(points):
            currentPoint = points[i]
            previousPoint = points[i - 1]
            distance = self.get_distance(previousPoint, currentPoint)
            if (distance == 0):
                i += 1
                continue

            if (d + distance) >= interval:
                qx = previousPoint.x + ((interval - d) / distance) * (
                    currentPoint.x - previousPoint.x
                )
                qy = previousPoint.y + ((interval - d) / distance) * (
                    currentPoint.y - previousPoint.y
                )
                point = Point2D(qx, qy)
                newPoints.append(point)
                points.insert(i, point)
                d = 0.0
            else:
                d += distance

            i += 1

        if len(newPoints) == (self.NumPointsInGesture - 1):
            newPoints.append(points[-1])

        return newPoints

    def path_length(self, points: list):
        distance = 0.0
        for i in range(1, len(points)):
            distance += self.get_distance(points[i - 1], points[i])
        return distance

    def get_distance(self, p1: Point2D, p2: Point2D):
        dX = p2.x - p1.x
        dY = p2.y - p1.y
        distance = math.sqrt((dX * dX) + (dY * dY))
        return distance

    # TODO: template type
    def distance_at_best_angle(self, points: list(), template):
        startRange = -self.AngleRange
        endRange = self.AngleRange
        x1 = self.GoldenRatio * startRange + (1.0 - self.GoldenRatio) * endRange
        f1 = self.distance_at_angle(points, template, x1)
        x2 = (1.0 - self.GoldenRatio) * startRange + self.GoldenRatio * endRange
        f2 = self.distance_at_angle(points, template, x2)

        while abs(endRange - startRange) > self.AnglePrecision:
            if f1 < f2:
                endRange = x2
                x2 = x1
                f2 = f1
                x1 = self.GoldenRatio * startRange + (1.0 - self.GoldenRatio) * endRange
                f1 = self.distance_at_angle(points, template, x1)
            else:
                startRange = x1
                x1 = x2
                f1 = f2
                x2 = (1.0 - self.GoldenRatio) * startRange + self.GoldenRatio * endRange
                f2 = self.distance_at_angle(points, template, x2)

        return min(f1, f2)

    # TODO: template type
    def distance_at_angle(self, points: list(), template, rotation: float):
        newPoints = self.rotate_by(points, rotation)
        return self.path_distance(newPoints, template.Path)

    def path_distance(self, pts1: float, pts2: float):
        if len(pts1) != len(pts2):
            return float("inf")

        distance = sum([self.get_distance(pts1[i], pts2[i]) for i in range(len(pts1))])
        return distance / len(pts1)


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.Width = width
        self.Height = height


class RecognitionResult:
    def __init__(self, name: str, score: float):
        self.Name = name
        self.Score = score