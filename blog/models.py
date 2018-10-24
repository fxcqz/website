import re
import markdown2
from django.templatetags.static import static
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from .utils import display_list, random_colour


class ListItem(models.Model):
	title = models.CharField(max_length=280)
	url = models.TextField(blank=True, null=True)
	enabled = models.BooleanField(default=True)
	section = models.ForeignKey('Section', on_delete=models.SET_NULL,
								blank=True, null=True)
	background_image = models.FileField(blank=True, null=True)
	style = models.TextField(blank=True, help_text="One style per line")

	@property
	def display(self):
		if self.url:
			return '<a href="{}">{}</a>'.format(self.url, self.title)
		return self.title

	def get_style(self, colour_border=True):
		style = []
		if colour_border:
			style.append('border-bottom: 5px %s solid;' % random_colour())

		if self.section.section_type == Section.GRID and self.background_image:
			# really doesnt like string formatting for some reason
			style.append(
				'background-image: url(' + static('uploads/' + self.background_image.url) + ');'
			)
			style.extend([
				'color: #fff;',
				'font-weight: bold;'
				'text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;',
			])

		if self.style:
			style.extend('; '.join(self.style.split('\n')))

		return mark_safe(''.join(style))

	def __str__(self):
		section = self.section.title if self.section else "NONE"
		return '{} -> {} ({})'.format(
			section,
			self.title,
			'Enabled' if self.enabled else 'Disabled',
		)


class Post(models.Model):
	title = models.CharField(max_length=140)
	slug = models.SlugField(max_length=140)
	content = models.TextField()
	tags = models.TextField(blank=True, null=True)
	enabled = models.BooleanField(default=False)
	published = models.DateTimeField(blank=True, null=True)

	def get_style(self, colour_border=True):
		return mark_safe('min-height: 3rem')

	@property
	def display(self):
		return '<a href="%s">%s</a>' % (reverse('view_post', kwargs={'post': self.slug}), self.title)

	def __str__(self):
		return self.title

	@property
	def show_post(self):
		return mark_safe(markdown2.markdown(self.content))


class Section(models.Model):
	BLOB, LIST, GRID = 'BLOB', 'LIST', 'GRID'
	TYPE_CHOICES = (
		(BLOB, 'Blob'),
		(LIST, 'List'),
		(GRID, 'Grid'),
	)
	MODEL_CHOICES = (
		('POST', 'Posts'),
	)
	MODEL_MAP = {
		'POST': Post,
	}

	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50)
	tagline = models.CharField(max_length=280, blank=True)
	section_type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=BLOB)
	content = models.TextField(blank=True, null=True)
	sidebar = models.BooleanField(default=False)
	enabled = models.BooleanField(default=False)
	index = models.IntegerField(default=0)
	model_name = models.CharField(max_length=50, choices=MODEL_CHOICES, blank=True, null=True)

	def __str__(self):
		return self.title

	@property
	def display_content(self):
		result = []
		if self.tagline:
			result.append('<p>{}</p>'.format(self.tagline))

		if self.section_type in (self.LIST, self.GRID):
			if self.model_name:
				items = self.MODEL_MAP[self.model_name].objects.filter(enabled=True).order_by('-published')
			else:
				items = reversed(ListItem.objects.filter(section=self))

			if items:
				result.append(display_list(items, grid=self.section_type == self.GRID,
											colour=self.section_type == self.GRID))
			else:
				# require FK rather than ad hoc parsing
				result.append("")
		else:
			content = self.content
			if not re.search(r'<.*>', content, re.MULTILINE):
				# did not detect html content, so use nl2br
				content = linebreaks(content)
			result.append(content)

		return mark_safe('\n'.join(result))
