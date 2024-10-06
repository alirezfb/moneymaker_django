from django.db import models



class nmd46348559193224090(models.Model):
    datetime = models.DateField()
    number = models.IntegerField()
    qTitMeDem = models.IntegerField()
    zOrdMeDem = models.IntegerField()
    pMeDem = models.IntegerField()
    pMeOf = models.IntegerField()
    zOrdMeOf = models.IntegerField()
    qTitMeOf = models.IntegerField()

    def __str__(self):
        return f'{self.datetime} - {self.number} - {self.pMeOf}'


class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact phone', max_length=25)
    web = models.URLField('Website Address')
    email_address = models.EmailField('Email Address')

    def __str__(self):
        return self.name
class best_limits_2(models.Model):
    class Jooz:
        managed = False  # remove this line
        db_table = 'nmd46348559193224090'

class best_limits(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def save(self, *args, **kwargs):
        # Save the article using the 'db_write' database
        super().save(*args, **kwargs)

    def get_related_articles(self):
        # Perform a read query on the 'db_read' database
        return best_limits.objects.using('db_read')

class MoneymakerUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MoneymakerUser, blank=True)

    def __str__(self):
        return self.name
