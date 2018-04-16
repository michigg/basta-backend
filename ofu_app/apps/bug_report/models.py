# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO
import uuid
from _datetime import datetime

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_LENGTH = 256
MAX_TITLE_LENGTH = 128
MAX_DESCRIPTION_LENGTH = 1024
MAX_PRIORITY_LENGTH = 32
MAX_CATEGORY_LENGTH = 32
MAX_STATE_LENGTH = 64


# Create your models here.
class BugMsg(models.Model):
    # Priorities
    HIGH = 'HIGH'
    LOW = 'LOW'

    # Categories
    FOOD = 'FOOD'
    EVENTS = 'Events'
    DONAR = 'DONAR'
    OTHER = 'Other'

    # State
    REGISTERED = 'REGISTERED'
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    REJECTED = 'REJECTED'

    PRIORITY_CHOICES = (
        (HIGH, 'High'), (LOW, 'Low')
    )

    CATEGORY_CHOICES = (
        (FOOD, 'Food App'), (EVENTS, 'Event App'), (DONAR, 'Donar App'), (OTHER, 'Other')
    )

    STATE_CHOICES = (
        (REGISTERED, 'registered'), (TODO, 'todo'), (IN_PROGRESS, 'in progress'), (DONE, 'done'), (REJECTED, 'rejected')
    )

    # Api priorities data
    API_Priorities = [{'id': HIGH, 'name': 'High'},
                      {'id': LOW, 'name': 'Low'}, ]

    # Api categories data
    API_CATEGORIES = [{'id': FOOD, 'name': 'Food App', 'short': 'Food'},
                      {'id': EVENTS, 'name': 'Event App', 'short': 'Events'},
                      {'id': DONAR, 'name': 'Donar App', 'short': 'Donar'},
                      {'id': OTHER, 'name': 'Other', 'short': 'Other'}, ]

    # Api state data
    API_STATES = [{'id': REGISTERED, 'name': 'Registered'},
                  {'id': TODO, 'name': 'todo'},
                  {'id': IN_PROGRESS, 'name': 'in progress'},
                  {'id': DONE, 'name': 'done'},
                  {'id': REJECTED, 'name': 'rejected'},
                  ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH, unique=True)
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)
    priority = models.CharField(max_length=MAX_PRIORITY_LENGTH, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=MAX_CATEGORY_LENGTH, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=MAX_STATE_LENGTH, choices=STATE_CHOICES)
    registration_date = models.DateField(default=timezone.now)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.registration_date.strftime("%d.%m.%Y"), self.title, self.priority, self.status)
