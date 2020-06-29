"""
Holds the pynamodb Model for teams
"""
from pynamodb.models import Model
import pynamodb.attributes as attributes


class TeamModel(Model):
    class Meta:
        table_name = 'LowInkTeams'  # Table name on AWS
        region = 'eu-west-1'  # DB location
        read_capacity_units = 5  # Configures read capacity of DB
        write_capacity_units = 5  # Configures write capacity of DB
        # boto3 keys are dealt with via AWS CLI
    teamID = attributes.UnicodeAttribute(hash_key=True)
    teamName = attributes.UnicodeAttribute()
    captainDiscord = attributes.UnicodeAttribute()
    captainFC = attributes.UnicodeAttribute()
    captain = attributes.MapAttribute(default="Unknown")
    players = attributes.ListAttribute()
    checkIN = attributes.BooleanAttribute(default=False)
    allowCheckIN = attributes.BooleanAttribute(default=False)
    teamIconURL = attributes.UnicodeAttribute(default="Unknown")
