from django.db import models


class CanvasHistory(models.Model): # NOTE: later use celery_beat for get snapshot from canvas
    snapshot_time = models.DateTimeField(auto_now_add=True)
    pixels = models.JSONField()
    total_pixels_colored = models.PositiveBigIntegerField()
    active_users = models.PositiveIntegerField()

    def __str__(self):
        return f"Canvas Snapshot at {self.snapshot_time}"
