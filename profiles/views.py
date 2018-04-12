# Standard Library
import plistlib


# Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse, HttpResponseNotFound, HttpResponseBadRequest)
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import dateparse
from django.views.decorators.csrf import csrf_exempt


# Local
from models import Profile, Payload
from server import text_utils
from server import utils
from sal.decorators import *
from server.models import BusinessUnit, MachineGroup, Machine  # noqa: F811

# Create your views here.
@csrf_exempt
@key_auth_required
def submit_profiles(request):
    if request.method != 'POST':
        return HttpResponseNotFound('No POST data sent')

    submission = request.POST
    serial = submission.get('serial').upper()
    machine = None
    if serial:
        try:
            machine = Machine.objects.get(serial=serial)
        except Machine.DoesNotExist:
            return HttpResponseNotFound('Serial Number not found')

        compression_type = 'base64bz2'
        if 'base64bz2profiles' in submission:
            compressed_profiles = submission.get('base64bz2profiles')
        elif 'base64profiles' in submission:
            compressed_profiles = submission.get('base64bz2profiles')
            compression_type = 'base64'
        if compressed_profiles:
            compressed_profiles = compressed_profiles.replace(" ", "+")
            profiles_str = text_utils.decode_to_string(compressed_profiles, compression_type)
            try:
                profiles_list = plistlib.readPlistFromString(profiles_str)
            except Exception:
                profiles_list = None

            profiles_to_be_added = []
            machine.profile_set.all().delete()
            if '_computerlevel' in profiles_list:
                profiles_list = profiles_list['_computerlevel']
            for profile in profiles_list:
                parsed_date = dateparse.parse_datetime(profile.get('ProfileInstallDate'))
                profile_item = Profile(
                    machine = machine,
                    identifier = profile.get('ProfileIdentifier', ''),
                    display_name = profile.get('ProfileDisplayName', ''),
                    description = profile.get('ProfileDescription', ''),
                    organization = profile.get('ProfileOrganization', ''),
                    uuid = profile.get('ProfileUUID', ''),
                    verification_state = profile.get('ProfileVerificationState', ''),
                    install_date = parsed_date
                )

                if utils.is_postgres:
                    profiles_to_be_added.append(profile_item)
                else:
                    profile_item.save()

            if utils.is_postgres():
                Profile.objects.bulk_create(profiles_to_be_added)

            return HttpResponse("Profiles submitted for %s.\n" % 
                                submission.get('serial'))
    return HttpResponse("No profiles submitted.\n")
