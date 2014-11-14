from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control
from django_future.csrf import ensure_csrf_cookie

from courseware.courses import get_course_by_id
from edxmako.shortcuts import render_to_response
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from .models import PersonalOnlineCourse


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def dashboard(request, course_id):
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_by_id(course_key, depth=None)
    poc = get_poc_for_coach(course, request.user)
    context = {
        'course': course,
        'poc': poc,
    }
    if not poc:
        context['create_poc_url'] = reverse(
            'create_poc', kwargs={'course_id': course_id})
    return render_to_response('pocs/coach_dashboard.html', context)


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def create_poc(request, course_id):
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_by_id(course_key, depth=None)
    name = request.POST.get('name')
    poc = PersonalOnlineCourse(
        course_id=course.id,
        coach=request.user,
        display_name=name)
    poc.save()
    url = reverse('poc_coach_dashboard', kwargs={'course_id': course_id})
    return redirect(url)


def get_poc_for_coach(course, coach):
    """
    Looks to see if user is coach of a POC for this course.  Returns the POC or
    None.
    """
    try:
        return PersonalOnlineCourse.objects.get(
            course_id=course.id,
            coach=coach)
    except PersonalOnlineCourse.DoesNotExist:
        return None

