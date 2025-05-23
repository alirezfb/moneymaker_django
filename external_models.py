# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Nmd10024128313803797(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10024128313803797'


class Nmd10114441830266109(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10114441830266109'


class Nmd10120557300120078(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10120557300120078'


class Nmd10171945867136336(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10171945867136336'


class Nmd10191122735393627(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10191122735393627'


class Nmd10236455588057352(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10236455588057352'


class Nmd10411249540376641(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10411249540376641'


class Nmd10497143354080476(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10497143354080476'


class Nmd10568944722570445(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10568944722570445'


class Nmd10587006028472176(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd10587006028472176'


class Nmd11006334882585136(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11006334882585136'


class Nmd11129387075131725(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11129387075131725'


class Nmd11188958204590313(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11188958204590313'


class Nmd11214189898887899(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11214189898887899'


class Nmd11258722998911897(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11258722998911897'


class Nmd11326461864120062(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11326461864120062'


class Nmd11358107932902023(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11358107932902023'


class Nmd11403770140000603(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11403770140000603'


class Nmd11427387039523955(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11427387039523955'


class Nmd114312662654155(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd114312662654155'


class Nmd11432067920374603(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11432067920374603'


class Nmd11452654295102268(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    qtitmedem = models.IntegerField(db_column='qTitMeDem', blank=True, null=True)  # Field name made lowercase.
    zordmedem = models.IntegerField(db_column='zOrdMeDem', blank=True, null=True)  # Field name made lowercase.
    pmedem = models.IntegerField(db_column='pMeDem', blank=True, null=True)  # Field name made lowercase.
    pmeof = models.IntegerField(db_column='pMeOf', blank=True, null=True)  # Field name made lowercase.
    zordmeof = models.IntegerField(db_column='zOrdMeOf', blank=True, null=True)  # Field name made lowercase.
    qtitmeof = models.IntegerField(db_column='qTitMeOf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nmd11452654295102268'


class Nmd11622051128546106(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
