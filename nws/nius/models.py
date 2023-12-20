from django.db import models
from .newsy import trzy_doliny, rzadowe, mojrerpo, mojprow, efr, sow, unijne


# Create your models here.
class News(models.Model):
    tytul = models.CharField(max_length=100)
    opis = models.TextField()
    url = models.URLField()
    data = models.DateTimeField()
    source = models.URLField()
    is_new = models.BooleanField(default=True)
    day = models.DateField()

    def __str__(self):
        return self.tytul
    
    class Meta:
        verbose_name_plural ="Newsy"



trzy_doliny = trzy_doliny()
rzadowe = rzadowe()
unijne = unijne()
moj = mojrerpo()
prow = mojprow()
efr = efr()
sow = sow()

all_list = [moj, prow, trzy_doliny, rzadowe, efr, sow, unijne]

newsy_wszystkie=[]
for x in all_list:
    newsy_wszystkie.extend(x)
for news in newsy_wszystkie:
    if not News.objects.filter(url=news['link']).exists():
        News.objects.create(
            tytul=news['title'],
            opis=news['desc'],
            url=news['link'],
            data=news['date'],
            source = news['source'],
            day = news['date']
        )

