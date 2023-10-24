import operator

from django.db.models import Q

from .models import Talk


def create_info_list(user, friends):
    info = []
    info_have_message = []
    info_have_no_message = []

    for friend in friends:
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('-time')

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])

    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)

    info.extend(info_have_message)
    info.extend(info_have_no_message)

    return info