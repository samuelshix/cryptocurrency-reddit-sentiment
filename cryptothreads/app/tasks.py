from celery import shared_task



@shared_task(name='update_db')
def stuff():
    print('hi')