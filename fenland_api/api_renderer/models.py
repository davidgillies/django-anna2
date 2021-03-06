from datetime import date
from django.db import models


class Surgery(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    full_name = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    addr1 = models.CharField(max_length=45, blank=True)
    addr2 = models.CharField(max_length=45, blank=True)
    town = models.CharField(max_length=45, blank=True)
    county = models.CharField(max_length=45, blank=True)
    postcode = models.CharField(max_length=45, blank=True)
    telephone = models.CharField(max_length=12, blank=True)
    admin_contact_name = models.CharField(max_length=45, blank=True)
    admin_contact_number = models.CharField(max_length=45, blank=True)
    hscic_code = models.CharField(max_length=45, blank=True)
    area = models.CharField(max_length=45, blank=True)
    modified_by = models.CharField(max_length=45, blank=True)
    modified = models.DateTimeField(blank=True, null=True)
    surgeriescol = models.CharField(max_length=45, blank=True)

    def __unicode__(self):
        return "%s" % (self.full_name)

    class Meta:
        db_table = 'surgeries'
        verbose_name = 'Surgery'
        verbose_name_plural = 'Surgeries'


class Volunteer(models.Model):
    sex_types = (
        ('M', 'M'),
        ('F', 'F'),
    )
    title_types = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Miss', 'Miss'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
    )
    boolean_choices = (
        (1, 'True'),
        (2, 'False'),
        (3, 'None'),
    )

    id = models.AutoField(primary_key=True)  # AutoField?
    surname = models.CharField(max_length=45)
    forenames = models.CharField(max_length=45)
    initials = models.CharField(max_length=5, blank=True)
    dob = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=12, blank=True, choices=title_types)
    sex = models.CharField(max_length=1, blank=True, choices=sex_types)
    addr1 = models.CharField(max_length=45, blank=True)
    addr2 = models.CharField(max_length=45, blank=True)
    town = models.CharField(max_length=45, blank=True)
    county = models.CharField(max_length=45, blank=True)
    postcode = models.CharField(max_length=45, blank=True)
    home_tel = models.CharField(max_length=45, blank=True)
    work_tel = models.CharField(max_length=45, blank=True)
    mobile = models.CharField(max_length=45, blank=True)
    email = models.CharField(max_length=100, blank=True)
    nhs_no = models.CharField(max_length=45, blank=True)
    moved_away = models.IntegerField(blank=True, null=True, choices=boolean_choices)
    diabetes_diagnosed = models.IntegerField(blank=True, null=True, choices=boolean_choices)
    modified_by = models.CharField(max_length=45, blank=True)
    reason = models.IntegerField(blank=True, null=True)
    phase1_comment = models.TextField(blank=True)
    phase2_comment = models.TextField(blank=True)
    modified = models.DateTimeField(blank=True, null=True)
    surgeries = models.ForeignKey(Surgery, blank=True, null=True, default=4)

    def calculate_age(self):
        """Calculates age for the admin screens."""
        if self.dob:
            today = date.today()
            born = self.dob
            try:
                birthday = born.replace(year=today.year)
            except ValueError: # raised when birth date is February 29 and the current year is not a leap year
                birthday = born.replace(year=today.year, month=born.month+1, day=1)
            if birthday > today:
                age = today.year - born.year - 1
            else:
                age = today.year - born.year
            if age > 70:
                return '<span style="color: red;">%s</span>' % age
            else:
                return age
        else:
            return None

    calculate_age.allow_tags = True
    calculate_age.short_description = "Age"

    def __unicode__(self):
        return "%s, %s" % (self.surname, self.forenames)

    def __str__(self):
        return "%s, %s" % (self.surname, self.forenames)

    class Meta:
        db_table = 'volunteers'


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    repeat = models.IntegerField(blank=True, null=True)
    studyphase = models.IntegerField(blank=True, null=True)
    appt_date = models.DateField(blank=True, null=True)
    appt_time = models.TimeField(blank=True, null=True)
    test_site = models.CharField(max_length=10, blank=True)
    modified_by = models.CharField(max_length=45, blank=True)
    modified = models.DateTimeField(blank=True, null=True)
    volunteers = models.ForeignKey(Volunteer)

    def __unicode__(self):
        return "%s, %s, %s" % (self.volunteers.surname,
                               self.volunteers.forenames, self.appt_date)

    def __str__(self):
        return "%s, %s, %s" % (self.volunteers.surname,
                               self.volunteers.forenames, self.appt_date)

    class Meta:
        db_table = 'appointments'


class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    reason = models.TextField(blank=True)
    edit_date = models.DateField(blank=True, null=True)
    editor = models.CharField(max_length=45, blank=True)
    volunteers = models.ForeignKey(Volunteer)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Log'


class Status(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    curr_status = models.CharField(max_length=45, blank=True)
    volunteers = models.ForeignKey(Volunteer)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
