from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core import logger
from .selectors.pixel import show_canvas, show_pixel_range
from .services.pixel import paint_pixel
from .colors import get_enum_color
from .enums import Color
from .validators import validate_x_coordinates, validate_y_coordinates


class PixelListAPIView(APIView):
    """"get all or part of canvas"""
    # class CanvasOutputSerializer(serializers.Serializer):
    #     x = serializers.IntegerField()
    #     y = serializers.IntegerField()
    #     color = serializers.IntegerField()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="x_range",
                description="Range of x coordinates as `start,end`.",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="y_range",
                description="Range of y coordinates as `start,end`.",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": [
                        {"type": "integer", "example": 1},  # x coordinate
                        {"type": "integer", "example": 2},  # y coordinate
                        {"type": "integer", "example": 5},  # color as enum value
                    ],
                },
                "example": [[1, 1, 5], [1, 2, 6]],  # example response
            }
        },
    )
    def get(self, request):
        x_range = request.GET.get("x_range")
        y_range = request.GET.get("y_range")
        if x_range is None or y_range is None:
            canvas = show_canvas()
        else:
            try:
                x_start = int(x_range.split(",")[0])
                x_end = int(x_range.split(",")[1])
                y_start = int(y_range.split(",")[0])
                y_end = int(y_range.split(",")[1])

                canvas = show_pixel_range((x_start, x_end), (y_start, y_end))
            except Exception as e:
                logger.warn(f"can't read canvas with QueryParams:{e}")
                return Response(
                    {"detail": "Query params not's valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # srz = self.CanvasOutputSerializer(data=canvas,many=True)
        # srz.is_valid(raise_exception=True) # Using the serializer increases the execution time up to three times
        return Response(canvas)


class PixelPaintAPIView(APIView):
    """paint a pixel with enum of Color"""

    class PaintPixelInputSerializer(serializers.Serializer):
        x = serializers.IntegerField(validators=[validate_x_coordinates])
        y = serializers.IntegerField(validators=[validate_y_coordinates])
        color = serializers.IntegerField()

        def to_representation(self, instance):
            ret = super().to_representation(instance)

            color = get_enum_color(ret["color"])
            ret["color"] = color

            return ret

        def validate_color(self, value):
            color = get_enum_color(value)
            if color == Color.UNKNOWN:
                raise ValidationError("color is invalid")
            return value

    @extend_schema(
        request=PaintPixelInputSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "ok",
                    }
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "bad",
                    }
                },
            },
        },
    )
    def post(self, request):
        srz = self.PaintPixelInputSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        x = srz.data["x"]
        y = srz.data["y"]
        color = srz.data["color"]
        if paint_pixel(x, y, color):
            return Response({"status": "ok"})
        else:
            return Response(
                {"status": "bad"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
