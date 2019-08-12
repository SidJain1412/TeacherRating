from app import db
from .models import *


# Function to return average score
def average_score(current, existing, count):
    return ((existing * count) + current) / (count + 1)


def update_score(teacherId, dedication_score, leniency_score, marks_score, teaching_score, friendliness_score):
    rating_count = Rating.query.filter_by(teacher_id=teacherId).count()
    print('Teacher ' + str(teacherId) + ' has ' +
          str(rating_count) + ' ratings.')

    existing_ratings = Teacher.query.filter_by(id=teacherId).first()

    # printing names of all columns
    # print([cname for cname in existing_ratings.__dict__.keys()])

    existing_ratings.dedication_score = average_score(
        int(dedication_score), existing_ratings.dedication_score, rating_count)

    existing_ratings.leniency_score = average_score(
        int(leniency_score), existing_ratings.leniency_score, rating_count)

    existing_ratings.marks_score = average_score(
        int(marks_score), existing_ratings.marks_score, rating_count)

    existing_ratings.teaching_score = average_score(
        int(teaching_score), existing_ratings.teaching_score, rating_count)

    existing_ratings.friendliness_score = average_score(
        int(friendliness_score), existing_ratings.friendliness_score, rating_count)

    current_average = (int(dedication_score) + int(leniency_score) +
                       int(teaching_score) + int(marks_score) + int(friendliness_score)) / 5

    existing_ratings.overall_score = average_score(
        current_average, existing_ratings.overall_score, rating_count)

    db.session.commit()
    return True
