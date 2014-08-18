import time
from django.conf import settings
from django.db import models, connection

class ModProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mod_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100, blank=True, null=True)

class ActionStory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='action_stories')
    content = models.TextField()
    first_timestamp = models.IntegerField(default=lambda: int(time.time()))
    last_timestamp = models.IntegerField(default=lambda: int(time.time()), db_index=True)

    def write(self):
        def s(num_as_string):
            if (int(num_as_string) == 1):
                return ''
            else:
                return 's'

        # Write the story! Gather all the actions directly
        cursor = connection.cursor()
        cursor.execute("SELECT related_model, COUNT(*), SUM(points) FROM mcp_action WHERE story_id=" + str(self.id) + " GROUP BY related_model;")
        story_actions = cursor.fetchall()

        # Calculate points
        points = 0
        for actions in story_actions:
            points += int(actions[2])
        story = self.user.get_mini_name() + " earned " + "{:,}".format(points) + " point" + s(points) + " for reviewing"

        # Build the story
        story_parts = [' ' + str(action[1]) + ' ' + action[0].lower() + s(action[1]) for action in story_actions]

        if len(story_parts) > 1:
            story = story + ', '.join(story_parts[:-1]) + ' and ' + story_parts[-1] + '.'
        else:
            story = story + story_parts[-1] + '.'

        # Save the story
        self.content = story
        self.save()

    class Meta:
        ordering = ['-last_timestamp']

class ActionManager(models.Manager):
    def log(self, user, action_type, related_model, points, **kwargs):
        # First, we need to see if there is a recent story (30 minutes) to attach it to
        min_time = int(time.time()) - 1800 # 1800 = 30 mins in seconds
        stories = ActionStory.objects.filter(user=user, last_timestamp__gte=min_time)

        if stories:
            story = stories[0]
        else:
            story = ActionStory(user=user, content="")

        story.last_timestamp = int(time.time())
        story.save()

        # We have a story to attach it to, now we can create our action
        action = Action(user=user, action_type=action_type, related_model=related_model,
                        story=story, points=points, related_id=kwargs.get('related_id', None),
                        related_content=kwargs.get('related_content', None))
        action.save()

        # Now that we have saved the new action, let's regenerate the story content
        story.write()

class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions')
    action_type = models.CharField(max_length=50)
    related_model = models.CharField(max_length=50)
    related_id = models.IntegerField(blank=True, null=True)
    related_content = models.TextField(blank=True, null=True)
    timestamp = models.IntegerField(default=lambda: int(time.time()))
    story = models.ForeignKey(ActionStory, related_name='actions')
    points = models.IntegerField()

    objects = ActionManager()

    class Meta:
        ordering = ['-timestamp']

class Bulletin(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bulletins')
    timestamp = models.IntegerField(default=lambda: int(time.time()))
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_bulletins')

    class Meta:
        ordering = ['-timestamp']

    def check_read(self, user_id):
        return self.read_by.filter(id=user_id).count() != 0

class ShardCheckIn(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    district_id = models.IntegerField()
    channel = models.IntegerField()

    cpu_usage = models.CharField(max_length=50, blank=True, null=True)
    mem_usage = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    frame_rate = models.DecimalField(max_digits=8, decimal_places=5)
    heap_objects = models.IntegerField()
    heap_garbage = models.IntegerField()

    invasion = models.CharField(max_length=255, blank=True, null=True)
    population = models.IntegerField()

    timestamp = models.IntegerField(db_index=True)
    fetched = models.IntegerField(default=lambda: int(time.time()))

    class Meta:
        ordering = ['-timestamp']
