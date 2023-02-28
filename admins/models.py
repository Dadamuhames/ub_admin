from django.db import models
# telephone nbm validator

# messages
class Messages(models.Model):
    message_id = models.CharField('Message id', unique=True, max_length=255)
    user = models.CharField('User id', max_length=255)
    date = models.DateTimeField('Date')
    text = models.TextField()


# search quotes group
class SearchQuoteGroup(models.Model):
    name = models.CharField('Name', max_length=255)


# search quotes
class SearchQuotes(models.Model):
    quote = models.CharField('Quote', max_length=255)
    group = models.ForeignKey(SearchQuoteGroup, on_delete=models.CASCADE, related_name='quotes')

    