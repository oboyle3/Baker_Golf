from django.core.management.base import BaseCommand
from myapp.models import User, Golfer, UserAverage

class Command(BaseCommand):
    help = 'Update user averages based on selected golfers'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            selected_golfers = user.favorite_golfers.all()

            if selected_golfers:
                total_over_par = 0
                count = 0

                for golfer in selected_golfers:
                    scores = [golfer.day_1_score, golfer.day_2_score, golfer.day_3_score, golfer.day_4_score]
                    over_par = [score - 72 for score in scores if score is not None]

                    if over_par:
                        avg = sum(over_par) / len(over_par)
                        total_over_par += avg
                        count += 1

                if count > 0:
                    overall_avg = total_over_par / count

                    UserAverage.objects.update_or_create(
                        user=user,
                        defaults={'overall_avg_over_par': overall_avg}
                    )
        self.stdout.write(self.style.SUCCESS('Successfully updated user averages'))
