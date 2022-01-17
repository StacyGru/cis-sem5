from django.db import models
from viewflow.fields import CompositeKey

GENDER_CHOICES = [
    ('Ж', 'женский'),
    ('М', 'мужской')
]


PASSPORT_TYPE_CHOICES = [
    ('российский', 'российский'),
    ('заграничный', 'заграничный')
]

ROOM_TYPE_CHOICES = [
    ('одноместный', 'одноместный'),
    ('двухместный (с одной кроватью)', 'двухместный (с одной кроватью)'),
    ('двухместный (с двумя отдельными кроватями)', 'двухместный (с двумя отдельными кроватями)'),
    ('трёхместный (с одной кроватью для двоих + 1 доп. кроватью)', 'трёхместный (с одной кроватью для двоих + 1 доп. кроватью)'),
    ('четырёхместный (с одной кроватью для двоих + 2 доп. кроватями)', 'четырёхместный (с одной кроватью для двоих + 2 доп. кроватями)')
]

TRANSACTION_CHOICES = [
    ('добавление', 'добавление'),
    ('редактирование', 'редактирование'),
]


class Country(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'country'

    def __str__(self):
        return self.name


class City(models.Model):
    city = models.CharField(max_length=64)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country')

    class Meta:
        managed = False
        db_table = 'city'

    def __str__(self):
        return self.city


class ClientStatus(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'client_status'

    def __str__(self):
        return self.name


class Client(models.Model):
    surname = models.CharField(max_length=64)
    first_middle_name = models.CharField(db_column='first&middle_name', max_length=128)  # Field renamed to remove unsuitable characters.
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=256)
    status = models.ForeignKey(ClientStatus, models.DO_NOTHING, db_column='status')

    class Meta:
        managed = False
        db_table = 'client'

    def __str__(self):
        return self.surname


class Organization(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'organization'

    def __str__(self):
        return self.name


class Contract(models.Model):
    date_time = models.DateTimeField(db_column='date&time')  # Field renamed to remove unsuitable characters.
    preliminary_agreement_number = models.ForeignKey('PreliminaryAgreement', models.DO_NOTHING, db_column='preliminary_agreement_number')
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization')
    employee = models.ForeignKey('Employee', models.DO_NOTHING, db_column='employee')
    trip_participants = models.ForeignKey(Client, models.DO_NOTHING, db_column='trip_participants')
    currency = models.ForeignKey('CurrencyRate', models.DO_NOTHING, db_column='currency')
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'contract'

    def __str__(self):
        return str(self.id)


class CurrencyRate(models.Model):
    currency_name = models.CharField(max_length=64)
    amount = models.IntegerField()
    rate = models.FloatField()

    class Meta:
        managed = False
        db_table = 'currency_rate'

    def __str__(self):
        return self.currency_name


class EmployeePosition(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'employee_position'

    def __str__(self):
        return self.name


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=False, blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.IntegerField(default=True)
    is_active = models.IntegerField(default=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class Employee(models.Model):
    surname = models.CharField(max_length=64)
    first_middle_name = models.CharField(db_column='first&middle_name', max_length=128)  # Field renamed to remove unsuitable characters.
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    position = models.ForeignKey(EmployeePosition, models.DO_NOTHING, db_column='position')
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    user_auth = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='user_auth')

    class Meta:
        managed = False
        db_table = 'employee'

    def __str__(self):
        return self.surname


class Activity(models.Model):
    user_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    day_activity = models.BooleanField(default=False)
    night_activity = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'activity'

    def __str__(self):
        return self.user_id.__str__()


class TransactionLogEmployee(models.Model):
    type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    date_time = models.DateTimeField()
    employee_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transaction_log_employee'

    def __str__(self):
        return str(self.id)


class Hotel(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country')
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city')
    hotel_name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    number_of_stars = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'hotel'

    def __str__(self):
        return self.hotel_name


class TravelRoute(models.Model):
    preliminary_agreement_number = models.ForeignKey('PreliminaryAgreement', models.DO_NOTHING, db_column='preliminary_agreement_number')
    city_to_visit = models.ForeignKey(City, models.DO_NOTHING, db_column='city_to_visit')
    cities_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'travel_route'

    def __str__(self):
        return str(self.city_to_visit)


class HotelReservation(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING, db_column='hotel')
    contract_number = models.ForeignKey(Contract, models.DO_NOTHING, db_column='contract_number')
    travel_route = models.ForeignKey(TravelRoute, models.DO_NOTHING, db_column='travel_route')
    hotel_room = models.IntegerField()
    room_type = models.CharField(max_length=128, choices=ROOM_TYPE_CHOICES)
    check_in_date = models.DateField(db_column='check-in_date')  # Field renamed to remove unsuitable characters.
    check_out_date = models.DateField()
    currency = models.ForeignKey(CurrencyRate, models.DO_NOTHING, db_column='currency')
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hotel_reservation'

    def __str__(self):
        return str(self.id)


class Passport(models.Model):
    id = CompositeKey(columns=['series', 'number'])
    series = models.IntegerField()
    number = models.IntegerField()
    client = models.ForeignKey(Client, models.DO_NOTHING)
    passport_type = models.CharField(max_length=15, choices=PASSPORT_TYPE_CHOICES)
    date_of_issue = models.DateField()
    expiration_date = models.DateField()
    issued_by = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'passport'

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    date_time = models.DateTimeField(db_column='date&time')  # Field renamed to remove unsuitable characters.
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization')
    contract_number = models.ForeignKey(Contract, models.DO_NOTHING, db_column='contract_number')
    sum_in_rubles = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'

    def __str__(self):
        return str(self.id)


class PreliminaryAgreement(models.Model):
    date_time = models.DateTimeField(db_column='date&time')  # Field renamed to remove unsuitable characters.
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization')
    employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='employee')
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client')
    number_of_trip_participants = models.IntegerField()
    country_to_visit = models.ForeignKey(Country, models.DO_NOTHING, db_column='country_to_visit', blank=True, null=True)
    trip_start_date = models.DateField()
    trip_end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'preliminary_agreement'

    def __str__(self):
        return str(self.id)


class Synchronization(models.Model):
    date_time = models.DateTimeField(db_column='date&time')  # Field renamed to remove unsuitable characters.
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization')
    file = models.TextField()

    class Meta:
        managed = False
        db_table = 'synchronization'

    def __str__(self):
        return str(self.date_time)


class Trip(models.Model):
    contract_number = models.ForeignKey(Contract, models.DO_NOTHING, db_column='contract_number')
    departure_place = models.CharField(max_length=128)
    arrival_place = models.CharField(max_length=128)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    transport_type = models.CharField(max_length=7)
    transfer = models.IntegerField()
    travel_document_number = models.IntegerField()
    currency = models.ForeignKey(CurrencyRate, models.DO_NOTHING, db_column='currency')
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trip'

    def __str__(self):
        return str(self.contract_number)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
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
