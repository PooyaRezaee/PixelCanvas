from django.core.management.base import BaseCommand
from core import logger
from ...repositories.redis_operation import save_pixel, r


class Command(BaseCommand):
    help = "Creates a 100x100 canvas in Redis with initial value of 1 (representing white color)"

    def handle(self, *args, **options):
        pipeline = r.pipeline()
        for x in range(100):
            for y in range(100):
                try:
                    save_pixel(x, y, 1, pipeline)
                except Exception as e:
                    logger.error(f"Failed to save pixel ({x}, {y}): {e}")

        pipeline.execute()

        self.stdout.write(
            self.style.SUCCESS("Successfully created a 100x100 canvas in Redis")
        )
