from pynamodb.models import Model
import pynamodb.attributes as attributes


class TeamModel(Model):
    class Meta:
        table_name = 'LowInkTeams'
        region = 'eu-west-1'
        read_capacity_units = 5
        write_capacity_units = 5
    teamID = attributes.UnicodeAttribute(hash_key=True)
    teamName = attributes.UnicodeAttribute()
    captainDiscord = attributes.UnicodeAttribute()
    captainFC = attributes.UnicodeAttribute()
    captain = attributes.MapAttribute(default="Unknown")
    players = attributes.ListAttribute()
    checkIN = attributes.BooleanAttribute(default=False)
    teamIconURL = attributes.UnicodeAttribute(default="Unknown")
