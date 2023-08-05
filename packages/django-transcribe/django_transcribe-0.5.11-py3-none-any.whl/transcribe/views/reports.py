import csv
import logging
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware
from transcribe.models import Project, Task, TranscribeUser, UserTask

log = logging.getLogger(__name__)


class TaskReportHolder:
    def __init__(self):
        self.projects = []
        self.totals = TotalTaskCounter()


class TotalTaskCounter:
    def __init__(
        self,
        total_transcriptions=0,
        total_finished_transcriptions=0,
        total_reviewed=0,
    ):
        self.total_user_transcriptions = total_transcriptions
        self.total_finished_transcriptions = total_finished_transcriptions
        self.total_reviewed = total_reviewed
        self.total_ready_for_review = (
            self.total_finished_transcriptions - self.total_reviewed
        )

    def __iadd__(self, other):
        self.total_user_transcriptions += other.total_user_transcriptions
        self.total_finished_transcriptions += (
            other.total_finished_transcriptions
        )  # noqa
        self.total_reviewed += other.total_reviewed
        self.total_ready_for_review += other.total_ready_for_review
        return self

    @staticmethod
    def _query_count(
        project, start_date, end_date, for_tasks=False, **filters
    ):
        value = 'task__id' if for_tasks else 'id'
        query = (
            UserTask.objects.filter(task__project=project)
            .filter(modified__range=[start_date, end_date])
            .filter(**filters)
            .values(value)
            .annotate(tcount=Count(value))
            .order_by('tcount')
        )

        return query.count()

    @classmethod
    def from_project(cls, project, start_date, end_date):
        end_date = end_date + timedelta(days=1)
        params = {
            'project': project,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'finished',
            'task_type': 'transcription',
        }

        total_transcriptions = cls._query_count(**params)

        tasks = Task.objects.filter(
            project=project
        ).annotate_num_finished_usertasks()

        tpt = project.transcribers_per_task
        total_finished_transcriptions = (
            tasks.filter(num_finished_transcriptions__gte=tpt)
            .annotate_last_transcribed()
            .filter(last_transcribed__range=[start_date, end_date])
        )
        total_finished_transcriptions = total_finished_transcriptions.count()
        total_reviewed = (
            tasks.filter(num_finished_reviews__gte=1)
            .filter(modified__range=[start_date, end_date])
            .count()
        )

        totals = cls(
            total_transcriptions, total_finished_transcriptions, total_reviewed
        )
        return totals


@login_required
def reports_list(request):
    today = make_aware(datetime.today())
    first_of_month = datetime(day=1, month=today.month, year=today.year)
    previous_month = first_of_month - timedelta(days=1)
    first_of_previous_month = datetime(
        day=1, month=previous_month.month, year=previous_month.year
    )
    previous_month2 = first_of_previous_month - timedelta(days=1)

    data = {
        'current_month': {
            'month_name': today.strftime('%B %Y'),
            'datetime_start': today.strftime('%Y-%m-01 00:00:00'),
            'datetime_end': today.strftime('%Y-%m-%d 23:59:59'),
        },
        'previous_month': {
            'month_name': previous_month.strftime('%B %Y'),
            'datetime_start': previous_month.strftime('%Y-%m-01 00:00:00'),
            'datetime_end': previous_month.strftime('%Y-%m-%d 23:59:59'),
        },
        'previous_month2': {
            'month_name': previous_month2.strftime('%B %Y'),
            'datetime_start': previous_month2.strftime('%Y-%m-01 00:00:00'),
            'datetime_end': previous_month2.strftime('%Y-%m-%d 23:59:59'),
        },
    }
    return render(request, 'transcribe/reports/list.html', data)


@login_required
def projects_report(request):
    # user must be staff to view this
    if not request.user.is_staff:
        return HttpResponse(status=403)
    datetime_start = datetime.strptime(
        request.GET.get('datetime_start'), '%Y-%m-%d %H:%M:%S'
    )
    datetime_end = datetime.strptime(
        request.GET.get('datetime_end'), '%Y-%m-%d %H:%M:%S'
    )
    # make our datetimes timezone aware
    datetime_start = make_aware(datetime_start)
    datetime_end = make_aware(datetime_end)

    projects = (
        Project.objects.all()
    )  # all() gets all projects except the ones that are archived
    all_projects_total = {'transcriptions': 0, 'reviews': 0}
    for project in projects:
        project.stats = project.stats(datetime_start, datetime_end)
        all_projects_total['transcriptions'] += project.stats[
            'finished_transcriptions'
        ]
        all_projects_total['reviews'] += project.stats['finished_reviews']
    data = {
        'datetime_start': datetime_start,
        'datetime_end': datetime_end,
        'projects': projects,
        'all_projects_total': all_projects_total,
    }

    # download the report as a csv file
    download = request.GET.get('download', False)
    if download:
        filename = f"projects_report_{datetime_start.strftime('%B')}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Transcribe Projects'])
        writer.writerow(
            [
                f"{datetime_start.strftime('%Y-%m-%d %H:%M:%S')} - {datetime_end.strftime('%Y-%m-%d %H:%M:%S')}"
            ]
        )
        writer.writerow(['', ''])
        current_datetime = make_aware(datetime.today()).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        writer.writerow(
            [
                '',
                '',
                '',
                f'as of {current_datetime}',
                f'as of {current_datetime}',
                '',
            ]
        )
        writer.writerow(
            [
                'Project',
                'Transcriptions',
                'Reviews',
                'Total Finished Transcriptions',
                'Total Finished Reviews',
                'Total Tasks',
            ]
        )
        # totals for each project
        for project in projects:
            project_data = []
            project_data.append(project.title)
            project_data.append(project.stats['finished_transcriptions'])
            project_data.append(project.stats['finished_reviews'])
            project_data.append(project.stats['total_finished_transcriptions'])
            project_data.append(project.stats['total_finished_reviews'])
            project_data.append(project.stats['total_tasks'])
            writer.writerow(project_data)
        # totals for all projects
        # writer.writerow(['', ''])
        # writer.writerow(['all projects', f"{all_projects_total['transcriptions']}", f"{all_projects_total['reviews']}"])
        return response

    # show an html report
    return render(request, 'transcribe/reports/projects.html', data)


@login_required
def users_report(request):
    # user must be staff to view this
    if not request.user.is_staff:
        return HttpResponse(status=403)
    datetime_start = datetime.strptime(
        request.GET.get('datetime_start'), '%Y-%m-%d %H:%M:%S'
    )
    datetime_end = datetime.strptime(
        request.GET.get('datetime_end'), '%Y-%m-%d %H:%M:%S'
    )
    # make our datetimes timezone aware
    datetime_start = make_aware(datetime_start)
    datetime_end = make_aware(datetime_end)

    # list of users
    users = TranscribeUser.objects.filter(last_login__gte=datetime_start)
    # get stats for each user
    for user in users:
        user._get_report_stats(datetime_start, datetime_end)
    # remove users without any activity
    active_users = []
    for user in users:
        if (
            user.num_finished_transcriptions > 0
            or user.num_finished_reviews > 0
            or user.num_skipped_transcriptions > 0
            or user.num_skipped_reviews > 0
        ):
            active_users.append(user)
    users = []
    data = {
        'datetime_start': datetime_start,
        'datetime_end': datetime_end,
        'users': active_users,
    }

    # download the report as a csv file
    download = request.GET.get('download', False)
    if download:
        filename = f"users_report_{datetime_start.strftime('%B')}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Transcribe Users'])
        writer.writerow(
            [
                f"{datetime_start.strftime('%Y-%m-%d %H:%M:%S')} - {datetime_end.strftime('%Y-%m-%d %H:%M:%S')}"
            ]
        )
        writer.writerow(['', ''])
        writer.writerow(
            [
                'Name',
                'Username',
                'Transcriptions',
                'Skipped Transcriptions',
                'Reviews',
                'Skipped Reviews',
            ]
        )
        # totals for each project
        for user in active_users:
            user_data = []
            user_data.append(f'{user.last_name}, {user.first_name}')
            user_data.append(f'{user}')
            user_data.append(f'{user.num_finished_transcriptions}')
            user_data.append(f'{user.num_skipped_transcriptions}')
            user_data.append(f'{user.num_finished_reviews}')
            user_data.append(f'{user.num_skipped_reviews}')
            writer.writerow(user_data)
        return response

    # show an html report
    return render(request, 'transcribe/reports/users.html', data)
